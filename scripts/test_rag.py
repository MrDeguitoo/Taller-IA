import os
from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_DB", "./data/chroma")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

def probar_busqueda():
    print("Conectando a la base de datos vectorial...")
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    vector_store = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    
    # Probamos el retriever (buscador)
    query = "falla en el sistema de inyección"
    print(f"\nBuscando información para: '{query}'")
    
    resultados = vector_store.similarity_search(query, k=2)
    
    if not resultados:
        print("No se encontraron resultados. ¿Seguro que indexaste los documentos?")
        return

    print("\n--- RESULTADOS ENCONTRADOS ---")
    for i, doc in enumerate(resultados):
        print(f"\nDocumento {i+1} (Fuente: {doc.metadata.get('source', 'Desconocida')}):")
        print(doc.page_content)

if __name__ == "__main__":
    probar_busqueda()