"""
Dashboard de monitoreo en tiempo real para Taller IA (Evaluación 3 — IE5).

Consume métricas expuestas por FastAPI en GET /api/v1/metrics y las
visualiza con auto-refresh cada 3 segundos.

Uso:
    streamlit run scripts/dashboard.py
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
import streamlit as st

METRICS_URL = os.getenv("METRICS_URL", "http://localhost:8000/api/v1/metrics")
REFRESH_SECONDS = int(os.getenv("DASHBOARD_REFRESH_SECONDS", "3"))
MAX_HISTORY = int(os.getenv("DASHBOARD_MAX_HISTORY", "50"))


def fetch_metrics(url: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.ConnectionError:
        return None, "No se pudo conectar con FastAPI. ¿Está corriendo uvicorn en el puerto 8000?"
    except requests.Timeout:
        return None, "La API tardó demasiado en responder (timeout)."
    except requests.RequestException as exc:
        return None, f"Error al consultar métricas: {exc}"


def init_session_state() -> None:
    defaults = {
        "latency_history": [],
        "avg_history": [],
        "failed_history": [],
        "timestamps": [],
        "prev_failed": 0,
        "alerts": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def append_history(metrics: dict[str, Any]) -> None:
    now = datetime.now().strftime("%H:%M:%S")
    last_latency = metrics.get("last_latency_ms") or 0.0
    avg_latency = metrics.get("avg_latency_ms") or 0.0
    failed = metrics.get("requests_failed", 0)

    st.session_state.timestamps.append(now)
    st.session_state.latency_history.append(last_latency)
    st.session_state.avg_history.append(avg_latency)
    st.session_state.failed_history.append(failed)

    if len(st.session_state.timestamps) > MAX_HISTORY:
        st.session_state.timestamps.pop(0)
        st.session_state.latency_history.pop(0)
        st.session_state.avg_history.pop(0)
        st.session_state.failed_history.pop(0)

    if failed > st.session_state.prev_failed:
        delta = failed - st.session_state.prev_failed
        st.session_state.alerts.insert(
            0,
            {
                "time": now,
                "message": (
                    f"Se detectaron {delta} petición(es) fallida(s) nueva(s). "
                    "Posibles causas: Ollama no disponible, ChromaDB sin indexar o error de conexión."
                ),
            },
        )
        st.session_state.alerts = st.session_state.alerts[:10]

    st.session_state.prev_failed = failed


def render_alerts(failed: int, api_error: str | None) -> None:
    st.subheader("Alertas del sistema")

    if api_error:
        st.error(f"Backend no disponible — {api_error}")
        st.info("Levanta el backend con: `uvicorn app.main:app --reload`")
        return

    if failed > 0:
        st.warning(
            f"Hay **{failed}** petición(es) fallida(s) registrada(s). "
            "Revisa los logs del backend y verifica Ollama (`ollama list`) y ChromaDB."
        )
    else:
        st.success("Sin fallas registradas. El servicio RAG responde correctamente.")

    for alert in st.session_state.alerts:
        st.error(f"[{alert['time']}] {alert['message']}")


def main() -> None:
    st.set_page_config(
        page_title="Taller IA — Dashboard",
        page_icon="📊",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.5rem; }
        div[data-testid="stMetric"] {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.75rem;
            padding: 0.75rem 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    init_session_state()

    st.title("📊 Taller IA — Dashboard de Monitoreo")
    st.caption(
        f"Monitoreo en vivo del servicio RAG · Auto-refresh cada {REFRESH_SECONDS}s · "
        f"Fuente: `{METRICS_URL}`"
    )

    with st.sidebar:
        st.header("Configuración")
        metrics_url = st.text_input("URL de métricas", value=METRICS_URL)
        refresh = st.slider("Intervalo de refresh (seg)", 2, 10, REFRESH_SECONDS)
        st.divider()
        st.markdown("**Servicios requeridos**")
        st.markdown("- FastAPI → puerto 8000")
        st.markdown("- Ollama → modelos locales")
        st.markdown("- ChromaDB → indexado")

    metrics, api_error = fetch_metrics(metrics_url)

    col_status, col_updated = st.columns([3, 1])
    with col_status:
        if api_error:
            st.markdown("🔴 **Estado:** Desconectado")
        else:
            st.markdown("🟢 **Estado:** Conectado al backend")
    with col_updated:
        st.markdown(f"**Actualizado:** {datetime.now().strftime('%H:%M:%S')}")

    if metrics:
        append_history(metrics)

        total = metrics.get("requests_total", 0)
        success = metrics.get("requests_success", 0)
        failed = metrics.get("requests_failed", 0)
        avg_latency = metrics.get("avg_latency_ms", 0.0)
        last_latency = metrics.get("last_latency_ms")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total de peticiones", total)
        m2.metric("Peticiones exitosas", success)
        m3.metric("Peticiones fallidas", failed, delta=None if failed == 0 else f"+{failed}")
        success_rate = round((success / total) * 100, 1) if total else 0.0
        m4.metric("Tasa de éxito", f"{success_rate}%")

        st.divider()

        chart_col, bar_col = st.columns(2)

        with chart_col:
            st.subheader("Evolución de latencia (ms)")
            if st.session_state.timestamps:
                df_line = pd.DataFrame(
                    {
                        "Última latencia": st.session_state.latency_history,
                        "Latencia promedio": st.session_state.avg_history,
                    },
                    index=st.session_state.timestamps,
                )
                st.line_chart(df_line, use_container_width=True)
            else:
                st.info("Esperando datos de latencia…")

        with bar_col:
            st.subheader("Latencia actual (comparativa)")
            if last_latency is not None:
                df_bar = pd.DataFrame(
                    {
                        "ms": [avg_latency, last_latency],
                    },
                    index=["Promedio", "Última consulta"],
                )
                st.bar_chart(df_bar, use_container_width=True)
            else:
                st.info("Aún no hay consultas RAG registradas.")

        st.divider()
        render_alerts(failed, api_error)

        with st.expander("JSON crudo de métricas"):
            st.json(metrics)
    else:
        render_alerts(0, api_error)

    st.caption(f"Próxima actualización automática en {refresh} segundos…")

    import time

    time.sleep(refresh)
    st.rerun()


if __name__ == "__main__":
    main()
