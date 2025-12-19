from app.orchestration.generic_responses import get_generic_response
from app.rag.rag_answer import RAG_answer

def orchestrated_answer(question: str) -> str:
    """
    Orquestador principal:
    Busca respuesta fija y si no hay, pasa a RAG
    """
    fixed = get_generic_response(question)

    if fixed:
        return fixed

    return RAG_answer(question)