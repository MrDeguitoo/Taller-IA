from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Importar nuestros routers
from app.routers import diagnostico_router

load_dotenv()

app = FastAPI(title="Taller Automotriz Inteligente API", version="2.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar (conectar) los routers
app.include_router(diagnostico_router.router)

@app.get("/")
def home():
    return {"status": "API modularizada funcionando correctamente"}