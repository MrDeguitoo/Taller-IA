# 🔧 Sistema Inteligente de Traducción de Diagnósticos Mecánicos con IA y RAG

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-green?logo=chainlink)](https://python.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-LLaMA_3.1_8B-orange)](https://ollama.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5-purple)](https://www.trychroma.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-teal?logo=fastapi)](https://fastapi.tiangolo.com/)

## 📋 Descripción del Proyecto

Este proyecto corresponde a una solución basada en Inteligencia Artificial, modelos LLM y técnicas RAG orientada a mejorar la comunicación entre talleres mecánicos y sus clientes.

El sistema permite traducir diagnósticos automotrices técnicos a un lenguaje simple y comprensible utilizando documentos reales del taller, historial de reparaciones y manuales automotrices como base de conocimiento.

La solución utiliza un pipeline de Recuperación Aumentada por Generación (RAG) junto con un modelo LLM ejecutado localmente mediante Ollama.

---

# Problema que Resuelve

| Problema Detectado                          | Solución Implementada                   |
| ------------------------------------------- | --------------------------------------- |
| Clientes no entienden diagnósticos técnicos | Traducción automática a lenguaje simple |
| Desconfianza en reparaciones                | Explicaciones claras y entendibles      |
| Mucho tiempo explicando fallas              | Respuestas automáticas mediante IA      |
| Información técnica dispersa                | Centralización mediante RAG             |
| Riesgo de respuestas incorrectas            | Uso de contexto real recuperado         |

---

# Arquitectura del Sistema

```text
┌──────────────────────────────┐
│       Cliente / Mecánico     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Frontend Web            │
│    React + Tailwind          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Backend API          │
│          FastAPI             │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐   ┌────────────────┐
│   Motor RAG  │   │ Base de Datos  │
│  LangChain   │   │    SQLite      │
└──────┬───────┘   └────────────────┘
       │
       ▼
┌──────────────────────────────┐
│        ChromaDB              │
│      Base Vectorial          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  Documentos del Taller       │
│ - Informes técnicos          │
│ - Manuales PDF               │
│ - Historial de fallas        │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      LLM Local               │
│   LLaMA 3.1 + Ollama         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Respuesta Simplificada       │
│ para el Cliente              │
└──────────────────────────────┘
```

---

# Flujo General del Pipeline RAG

1. El usuario ingresa una consulta o diagnóstico técnico.
2. La consulta es convertida en embeddings.
3. ChromaDB busca los fragmentos más relevantes.
4. El contexto recuperado se inserta en el prompt.
5. LLaMA 3.1 genera una respuesta simplificada.
6. El cliente recibe una explicación clara y comprensible.

---

# Tecnologías Utilizadas

| Tecnología       | Función                    |
| ---------------- | -------------------------- |
| Python 3.11      | Backend principal          |
| FastAPI          | API REST                   |
| React            | Frontend                   |
| LangChain        | Orquestación RAG           |
| ChromaDB         | Base vectorial             |
| Ollama           | Ejecución local de modelos |
| LLaMA 3.1        | Modelo LLM                 |
| nomic-embed-text | Embeddings                 |
| SQLite           | Base de datos              |
| Docker           | Contenedores               |

---

# Ejecución del Proyecto

## 1. Clonar repositorio

```bash
git clone https://github.com/usuario/proyecto-taller-ia.git
cd proyecto-taller-ia
```

---

## 2. Crear entorno virtual

```bash
python -m venv venv
```

### Activar entorno

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\\Scripts\\activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Instalar Ollama

Descargar desde:

https://ollama.com

---

## 5. Descargar modelos

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

---

## 6. Configurar variables de entorno

Crear archivo `.env`

```env
OLLAMA_MODEL=llama3.1:8b
EMBED_MODEL=nomic-embed-text
CHROMA_DB=./data/chroma
SQLITE_DB=./data/database.db
```

---

## 7. Ejecutar indexación de documentos

```bash
python scripts/index_documents.py
```

---

## 8. Iniciar Backend

```bash
uvicorn app.main:app --reload
```

API disponible en:

```text
http://localhost:8000
```

---

## 9. Iniciar Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend disponible en:

```text
http://localhost:3000
```

---

# Estructura del Proyecto

```text
proyecto-taller-ia/
│
├── app/
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── prompts/
│   └── models/
│
├── frontend/
│
├── data/
│   ├── documentos/
│   └── chroma/
│
├── scripts/
│   ├── index_documents.py
│   └── test_rag.py
│
├── tests/
│
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

# Ejemplos de Uso

```text
Usuario:
Explícame qué significa falla en el sistema de inyección.

Respuesta:
El vehículo presenta un problema en el sistema que envía combustible al motor.
Esto puede provocar pérdida de potencia, consumo excesivo de combustible o dificultad para encender el automóvil.
Se recomienda revisar la bomba de combustible y los inyectores para evitar daños mayores.
```

---

# Beneficios Esperados

* Mejor comprensión por parte de los clientes.
* Mayor confianza en el taller.
* Reducción de tiempo explicando diagnósticos.
* Respuestas más rápidas y precisas.
* Uso de información real mediante RAG.
* Modernización de procesos del taller.

---

# Referencias Técnicas

* LangChain Documentation
* Ollama Documentation
* ChromaDB Documentation
* FastAPI Documentation
* Lewis et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.
