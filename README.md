# Taller IA — Traductor RAG de Diagnósticos Mecánicos

Sistema de inteligencia artificial para talleres mecánicos en Chile. Convierte diagnósticos técnicos en explicaciones simples para clientes, usando **RAG** (Retrieval-Augmented Generation) con modelos locales vía **Ollama**.

Todo el procesamiento de IA corre **100% local**: sin APIs de pago ni dependencias en la nube.

---

## Requisitos previos

Instala esto **antes** de clonar el repositorio:

| Herramienta | Versión mínima | Para qué sirve |
|---|---|---|
| [Python](https://www.python.org/downloads/) | 3.11+ | Backend FastAPI |
| [Node.js](https://nodejs.org/) | 18+ | Frontend React + Vite |
| [Ollama](https://ollama.com/download) | Última estable | LLM y embeddings locales |

Verifica que estén instalados:

```bash
python --version
node --version
npm --version
ollama --version
```

---

## Estructura del proyecto

```text
Taller-IA/
├── app/                        # Backend FastAPI
│   ├── main.py                 # Punto de entrada de la API
│   ├── core/
│   │   └── observability.py    # Logs, latencia y métricas (Eval 3)
│   ├── routers/
│   │   └── diagnostico_router.py
│   ├── services/
│   │   └── rag_service.py      # Pipeline RAG
│   ├── prompts/
│   │   └── templates.py
│   └── models/
│       └── schemas.py
├── frontend/                   # Frontend React + Vite + Tailwind
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js          # Proxy /api → localhost:8000
│   └── src/
│       ├── main.jsx
│       └── App.jsx
├── scripts/
│   ├── index_documents.py      # Indexa PDFs en ChromaDB
│   ├── test_rag.py             # Prueba búsqueda vectorial
│   └── dashboard.py            # Dashboard Streamlit (Eval 3 — IE5)
├── data/
│   └── documentos/             # Coloca aquí los PDFs del taller
├── requirements.txt
├── Dockerfile                  # Backend (Docker)
├── docker-compose.yaml
├── .env.example
└── instalar.bat                # Atajo de instalación en Windows
```

> **Nota:** No subas archivos de sistema operativo (`__MACOSX/`, `._*`, `.DS_Store`). Ya están en `.gitignore`.

---

## Configuración inicial (solo la primera vez)

### Paso 1 — Clonar e instalar dependencias Python

**Windows:**

```bash
git clone <URL-DEL-REPO>
cd Taller-IA
instalar.bat
```

**macOS / Linux:**

```bash
git clone <URL-DEL-REPO>
cd Taller-IA
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Paso 2 — Variables de entorno

Copia el archivo de ejemplo:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Contenido por defecto:

```env
OLLAMA_MODEL=llama3.1:8b
EMBED_MODEL=nomic-embed-text
CHROMA_DB=./data/chroma
```

### Paso 3 — Descargar modelos en Ollama

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
ollama list
```

### Paso 4 — Indexar documentos del taller

1. Coloca archivos **PDF** con documentación técnica en `data/documentos/`.
2. Ejecuta (con el entorno virtual activo):

```bash
python scripts/index_documents.py
```

Salida esperada:

```text
Buscando documentos PDF en ./data/documentos/...
Fragmentando textos para RAG...
Generando Embeddings con nomic-embed-text y guardando en ChromaDB...
¡Indexación exitosa! N fragmentos guardados en ChromaDB.
```

> Si no hay PDFs, el script avisará y no creará la base vectorial.

### Paso 5 — Instalar dependencias del frontend

```bash
cd frontend
npm install
cd ..
```

---

## Levantar el sistema (cada vez que quieras usarlo)

Necesitas **3 terminales** como mínimo (4 si usas el dashboard de monitoreo).

### Terminal 1 — Ollama

```bash
ollama serve
```

> Si `ollama list` ya funciona, Ollama está corriendo y puedes saltar este paso.

### Terminal 2 — Backend (FastAPI)

**Windows:**

```bash
venv\Scripts\activate
uvicorn app.main:app --reload
```

**macOS / Linux:**

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Verifica:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

### Terminal 3 — Frontend (React + Vite)

```bash
cd frontend
npm run dev
```

Abre: http://localhost:5173

El proxy de Vite redirige `/api/*` hacia `http://localhost:8000` (sin problemas de CORS).

### Terminal 4 (opcional) — Dashboard de monitoreo (Evaluación 3 / IE5)

Con el backend corriendo, abre otra terminal en la raíz del proyecto:

**Windows:**

```bash
venv\Scripts\activate
streamlit run scripts/dashboard.py
```

**macOS / Linux:**

```bash
source venv/bin/activate
streamlit run scripts/dashboard.py
```

Abre el dashboard en: **http://localhost:8501**

El dashboard consume en tiempo real el endpoint `GET /api/v1/metrics` y se actualiza automáticamente cada 3 segundos.

---

## 📊 Monitoreo y Observabilidad

El sistema incluye observabilidad en dos capas:

| Capa | Componente | Descripción |
|---|---|---|
| Backend | `app/core/observability.py` | Registra latencia, errores y contadores en memoria |
| API | `GET /api/v1/metrics` | Expone las métricas en JSON |
| Dashboard | `scripts/dashboard.py` | Visualización en vivo con Streamlit |

### Métricas disponibles

- **Total de peticiones** — contador acumulado de consultas al RAG
- **Peticiones exitosas / fallidas** — desglose de resultados
- **Latencia promedio y última** — en milisegundos
- **Alertas visuales** — cuando aumentan las fallas (Ollama o ChromaDB)

### Levantar el dashboard

```bash
# Requisito: backend activo en http://localhost:8000
streamlit run scripts/dashboard.py
```

- **URL por defecto:** http://localhost:8501
- **Auto-refresh:** cada 3 segundos (configurable con `DASHBOARD_REFRESH_SECONDS`)
- **URL de métricas:** configurable con `METRICS_URL` (default: `http://localhost:8000/api/v1/metrics`)

### Verificar métricas desde terminal (sin dashboard)

```bash
curl http://localhost:8000/api/v1/metrics
```

---

## Cómo probar que todo funciona

### Health check

```bash
curl http://localhost:8000/
```

### Traducir un diagnóstico

```bash
curl -X POST http://localhost:8000/api/v1/traducir -H "Content-Type: application/json" -d "{\"diagnostico\": \"Falla en el sistema de inyección por baja presión de combustible\"}"
```

### Ver métricas (Evaluación 3)

```bash
curl http://localhost:8000/api/v1/metrics
```

### Probar búsqueda vectorial (sin API)

```bash
python scripts/test_rag.py
```

### Interfaz web

1. Abre http://localhost:5173
2. Escribe un diagnóstico técnico.
3. Clic en **Traducir para el Cliente**.

---

## Endpoints de la API

| Método | Ruta | Descripción |
|---|---|---|
| GET | / | Health check |
| POST | /api/v1/traducir | Traduce diagnóstico técnico a lenguaje simple |
| GET | /api/v1/metrics | Métricas de latencia, errores y contadores |

---

## Observabilidad (Evaluación 3)

El módulo `app/core/observability.py` registra:

- **Latencia** de cada consulta RAG (promedio y última, en ms)
- **Errores** clasificados: `ollama`, `chromadb`, `connection`, `unknown`
- **Contadores** de peticiones totales, exitosas y fallidas

Logs en consola del backend:

```text
2026-07-08 14:30:00 | INFO | taller_ia | Consulta RAG exitosa | latencia=2340.5 ms
2026-07-08 14:30:15 | ERROR | taller_ia | Consulta RAG fallida | tipo=ollama | ...
```

---

## Solución de problemas

| Síntoma | Solución |
|---|---|
| Frontend no carga | `cd frontend && npm install` |
| Error 404 en traducir | Usar `/api/v1/traducir` (corregido en App.jsx) |
| Error 500 | Verificar que Ollama esté corriendo (`ollama list`) |
| Sin documentos | PDFs en `data/documentos/` + `python scripts/index_documents.py` |
| Modelo no encontrado | `ollama pull llama3.1:8b` y `ollama pull nomic-embed-text` |
| Dashboard sin datos | Levantar backend primero, luego `streamlit run scripts/dashboard.py` |
| Dashboard no conecta | Verificar que FastAPI responda en http://localhost:8000/api/v1/metrics |

---

## Docker (opcional)

```bash
docker compose up --build
```

Requiere Ollama corriendo en la máquina host.

---

## Orden de inicio

```text
1. Ollama (serve + modelos descargados)
2. Indexar documentos (solo la primera vez)
3. Backend   →  uvicorn app.main:app --reload
4. Frontend  →  cd frontend && npm run dev
5. Dashboard →  streamlit run scripts/dashboard.py  (opcional, puerto 8501)
```
