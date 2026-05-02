from pydantic import BaseModel

# Lo que el cliente envía a la API
class QueryRequest(BaseModel):
    diagnostico: str

# Lo que la API le responde al cliente
class QueryResponse(BaseModel):
    diagnostico_original: str
    explicacion: str