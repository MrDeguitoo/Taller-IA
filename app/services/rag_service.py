import os

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

from app.core.observability import observability
from app.prompts.templates import prompt_traductor


class RagService:
    def __init__(self) -> None:
        chroma_path = os.getenv("CHROMA_DB", "./data/chroma")
        ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        embed_model = os.getenv("EMBED_MODEL", "nomic-embed-text")

        self.llm = Ollama(model=ollama_model)
        self.embeddings = OllamaEmbeddings(model=embed_model)
        self.vector_store = Chroma(
            persist_directory=chroma_path,
            embedding_function=self.embeddings,
        )
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        combine_docs_chain = create_stuff_documents_chain(self.llm, prompt_traductor)
        self.rag_chain = create_retrieval_chain(self.retriever, combine_docs_chain)

    def traducir(self, diagnostico: str) -> str:
        with observability.track_rag():
            response = self.rag_chain.invoke({"input": diagnostico})
            return response["answer"]


rag_service = RagService()
