from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import DATA_DIR

#DEFINIMOS LAS RUTAS DE LOS ARCHIVOS DE ENTRADA Y SALIDA
INPUT_PATH = DATA_DIR / "extracted_text" / "AAO_PPP_2025_AMD_raw.txt"
OUTPUT_PATH = DATA_DIR / "chunks" / "AAO_PPP_2025_AMD_chunks.txt"


text = INPUT_PATH.read_text(encoding="utf-8", errors="ignore")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=[
        "\n\n",
        "\n",
        ".",
        " ",
        ""
    ]
)

chunks = text_splitter.split_text(text)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_PATH.open("w", encoding="utf-8") as f:
    for i, chunk in enumerate(chunks, 1):
        f.write(f"\n\n{'#' * 80}\n")
        f.write(f"CHUNK {i}\n")
        f.write(f"{'#' * 80}\n\n")
        f.write(chunk)

print(f"Total de chunks generados: {len(chunks)}")