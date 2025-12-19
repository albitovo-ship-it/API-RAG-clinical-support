from pathlib import Path
import fitz #MODULO DE PyMuPDF


#DEFINIMOS LAS RUTAS DE LOS ARCHIVOS DE ENTRADA Y SALIDA
RAW_PDFS_DIR = Path("data/raw_pdfs")
OUTPUT_TEXT_DIR = Path("data/extracted_text")

#DEFINIMOS LA FUNCIÓN DE EXTRACCIÓN DE TEXTO DEL PDF
def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extrae texto de un PDF página por página usando PyMuPDF.
    """
    text_pages = []

    with fitz.open(pdf_path) as doc:
        for page_number, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            text_pages.append(
                f"\n\n--- Página {page_number} ---\n\n{page_text}"
            )

    return "".join(text_pages)


#DEFINIMOS LA FUNCIÓN PARA EJECUTAR EXTRACT_TEXT_FROM_PDF A TODOS LOS PDF DE LA CARPETA FUENTE
def process_all_pdfs():
    """
    Procesa todos los PDFs y guarda los textos extraídos.
    """
    OUTPUT_TEXT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(RAW_PDFS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No se encontraron PDFs en data/raw_pdfs.")
        return

    for pdf_path in pdf_files:
        print(f"Procesando: {pdf_path.name}")

        extracted_text = extract_text_from_pdf(pdf_path)

        output_file = OUTPUT_TEXT_DIR / f"{pdf_path.stem}_raw.txt"
        output_file.write_text(extracted_text, encoding="utf-8")

        print(f"Texto guardado en: {output_file}")


if __name__ == "__main__":
    process_all_pdfs()