from dotenv import load_dotenv
import os
import cohere
from chromadb import PersistentClient
from app.core.config import CHROMA_DIR

#CARGAMOS LA APIKEY
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

#CONECTAMOS CON COHERE
co = cohere.ClientV2(COHERE_API_KEY)

#CONECTAMOS A CHROMA DB
chroma_client = PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_collection(name="aao_amd_test")

def reranked_retriever(query_text: str, top_n=20, top_k=5):
    """
    Devuelve una lista de chunks rerankeados (strings)
    """
    query_embedding = co.embed(
        texts=[query_text],
        model="embed-multilingual-v3.0",
        input_type="search_query",
        embedding_types=["float"]
    ).embeddings.float_[0]

    #Retrieval inicial
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n
    )

    documents = results.get("documents", [[]])[0]

    #Reranking
    rerank_response = co.rerank(
        model="rerank-multilingual-v3.0",
        query=query_text,
        documents=documents,
        top_n=top_k
    )

    #Seleccionar solo los documentos finales
    reranked_docs = [
        documents[r.index]
        for r in rerank_response.results
    ]

    return reranked_docs