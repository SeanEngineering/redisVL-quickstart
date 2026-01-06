from pydantic import BaseModel


class DocumentIn(BaseModel):
    id: str
    content: str


class SearchRequest(BaseModel):
    query: str
    k: int = 5
