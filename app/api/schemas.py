from pydantic import BaseModel


class UserQuery(BaseModel):
    question: str

class RAGResponse(BaseModel):
    answer: str