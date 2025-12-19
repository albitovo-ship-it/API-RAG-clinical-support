from fastapi import APIRouter, HTTPException
from app.orchestration.orchestrator import orchestrated_answer
from app.api.schemas import UserQuery

#DEFINIMOS ROUTER
router= APIRouter()

#DEFINIMOS EL ENDPOINT
@router.post("/ask_question")
async def ask(query: UserQuery):
    """
    Endpoint para recibir preguntas del usuario y generar respuestas.
    """
    try:
        final_response = orchestrated_answer(query.question)
        return {"response": final_response}
    except Exception as e:
        # Raise an error for any exceptions encountered during processing
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred. Please try again later. Error details: {e}"
        )