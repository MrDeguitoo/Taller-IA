from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_service import rag_service

router = APIRouter(prefix="/api/v1", tags=["Diagnósticos"])

@router.post("/traducir", response_model=QueryResponse)
async def traducir_diagnostico(request: QueryRequest):
    try:
        # Llama a la lógica de negocio (el servicio)
        explicacion = rag_service.traducir(request.diagnostico)
        
        return QueryResponse(
            diagnostico_original=request.diagnostico,
            explicacion=explicacion
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))