import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass
from threading import Lock
from typing import Generator

logger = logging.getLogger("taller_ia")


def setup_logging(level: int = logging.INFO) -> None:
    if logging.getLogger().handlers:
        return

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


@dataclass(frozen=True)
class MetricsSnapshot:
    requests_total: int
    requests_success: int
    requests_failed: int
    avg_latency_ms: float
    last_latency_ms: float | None


def classify_error(error: Exception) -> str:
    message = str(error).lower()
    error_name = type(error).__name__.lower()

    if "ollama" in message or "connection refused" in message:
        return "ollama"
    if "chroma" in message or "chroma" in error_name:
        return "chromadb"
    if "connect" in message or "connection" in error_name:
        return "connection"
    return "unknown"


class ObservabilityService:
    def __init__(self) -> None:
        self._lock = Lock()
        self.requests_total = 0
        self.requests_success = 0
        self.requests_failed = 0
        self._latency_total_ms = 0.0
        self._last_latency_ms: float | None = None

    def record_success(self, latency_ms: float) -> None:
        with self._lock:
            self.requests_total += 1
            self.requests_success += 1
            self._latency_total_ms += latency_ms
            self._last_latency_ms = latency_ms

        logger.info("Consulta RAG exitosa | latencia=%.1f ms", latency_ms)

    def record_failure(
        self,
        error: Exception,
        latency_ms: float,
        *,
        context: str = "rag",
    ) -> str:
        error_type = classify_error(error)

        with self._lock:
            self.requests_total += 1
            self.requests_failed += 1
            self._last_latency_ms = latency_ms

        logger.error(
            "Consulta RAG fallida | tipo=%s | contexto=%s | latencia=%.1f ms | error=%s",
            error_type,
            context,
            latency_ms,
            error,
        )
        return error_type

    def get_metrics(self) -> MetricsSnapshot:
        with self._lock:
            avg_latency = (
                self._latency_total_ms / self.requests_success
                if self.requests_success
                else 0.0
            )
            return MetricsSnapshot(
                requests_total=self.requests_total,
                requests_success=self.requests_success,
                requests_failed=self.requests_failed,
                avg_latency_ms=round(avg_latency, 2),
                last_latency_ms=(
                    round(self._last_latency_ms, 2)
                    if self._last_latency_ms is not None
                    else None
                ),
            )

    @contextmanager
    def track_rag(self) -> Generator[None, None, None]:
        start = time.perf_counter()
        try:
            yield
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.record_failure(exc, elapsed_ms, context="rag_chain")
            raise
        else:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.record_success(elapsed_ms)


observability = ObservabilityService()
