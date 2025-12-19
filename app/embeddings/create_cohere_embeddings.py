from pathlib import Path
import os
import cohere
from cohere import Client
import chromadb
from chromadb import PersistentClient
from dotenv import load_dotenv
from app.core.config import DATA_DIR, CHROMA_DIR

#CARGAMOS LA APIKEY
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

#CONECTAMOS CON COHERE
co = cohere.ClientV2()

INPUT_PATH = DATA_DIR / "chunks" / "AAO_PPP_2025_AMD_chunks.txt"
COLLECTION_NAME = "aao_amd_test"

text = INPUT_PATH.read_text(encoding="utf-8", errors="ignore")

chunks_text = [c.strip() for c in text.split("CHUNK") if c.strip()]

print(f"Chunks detectados: {len(chunks_text)}")

#CREAMOS LOS EMBEDDINGS CON COHERE
response = co.embed(
    texts=chunks_text,
    model="embed-multilingual-v3.0",
    input_type="search_document",
    embedding_types=["float"]
)

embeddings = response.embeddings.float_

chroma_client = PersistentClient(path=str(CHROMA_DIR))

collection = chroma_client.get_or_create_collection(
    name="aao_amd_test",
    metadata={"hnsw:space": "cosine"}
)

collection.add(
    documents=chunks_text,
    embeddings=embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks_text))]
)

print("Embeddings guardados en Chroma")