from pydantic import BaseModel


class QueryRequest(BaseModel):
    diagnostico: str


class QueryResponse(BaseModel):
    diagnostico_original: str
    explicacion: str


class MetricsResponse(BaseModel):
    requests_total: int
    requests_success: int
    requests_failed: int
    avg_latency_ms: float
    last_latency_ms: float | None
