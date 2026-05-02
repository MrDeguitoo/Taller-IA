import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_DB", "./data/chroma")
DOCS_PATH = "./data/documentos"
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

def indexar_documentos():
    print(f"Buscando documentos PDF en {DOCS_PATH}...")
    loader = PyPDFDirectoryLoader(DOCS_PATH)
    documentos = loader.load()

    if not documentos:
        print("No se encontraron documentos. Asegúrate de poner PDFs en data/documentos/")
        return

    print("Fragmentando textos para RAG...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(documentos)

    print(f"Generando Embeddings con {EMBED_MODEL} y guardando en ChromaDB...")
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    
    Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH)
    print(f"¡Indexación exitosa! {len(chunks)} fragmentos guardados en ChromaDB.")

if __name__ == "__main__":
    os.makedirs(DOCS_PATH, exist_ok=True)
    indexar_documentos()