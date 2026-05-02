import os
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from app.prompts.templates import prompt_traductor

class RagService:
    def __init__(self):
        # Configuraciones
        CHROMA_PATH = os.getenv("CHROMA_DB", "./data/chroma")
        OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

        # Inicializar IA y Base Vectorial
        self.llm = Ollama(model=OLLAMA_MODEL)
        self.embeddings = OllamaEmbeddings(model=EMBED_MODEL)
        self.vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embeddings)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        # Armar la cadena
        combine_docs_chain = create_stuff_documents_chain(self.llm, prompt_traductor)
        self.rag_chain = create_retrieval_chain(self.retriever, combine_docs_chain)

    def traducir(self, diagnostico: str) -> str:
        # Ejecuta la consulta
        response = self.rag_chain.invoke({"input": diagnostico})
        return response["answer"]

# Instancia global del servicio para usarla en toda la app
rag_service = RagService()