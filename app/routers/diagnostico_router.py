from fastapi import APIRouter, HTTPException

from app.core.observability import classify_error, observability
from app.models.schemas import MetricsResponse, QueryRequest, QueryResponse
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/v1", tags=["Diagnósticos"])


@router.post("/traducir", response_model=QueryResponse)
async def traducir_diagnostico(request: QueryRequest) -> QueryResponse:
    try:
        explicacion = rag_service.traducir(request.diagnostico)
        return QueryResponse(
            diagnostico_original=request.diagnostico,
            explicacion=explicacion,
        )
    except Exception as exc:
        error_type = classify_error(exc)
        raise HTTPException(
            status_code=500,
            detail=f"Error en el servicio RAG ({error_type}): {exc}",
        ) from exc


@router.get("/metrics", response_model=MetricsResponse)
async def obtener_metricas() -> MetricsResponse:
    snapshot = observability.get_metrics()
    return MetricsResponse(
        requests_total=snapshot.requests_total,
        requests_success=snapshot.requests_success,
        requests_failed=snapshot.requests_failed,
        avg_latency_ms=snapshot.avg_latency_ms,
        last_latency_ms=snapshot.last_latency_ms,
    )
