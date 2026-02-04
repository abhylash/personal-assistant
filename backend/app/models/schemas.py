from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []
    session_id: str

class KnowledgeDocument(BaseModel):
    content: str
    title: Optional[str] = None
    metadata: Optional[dict] = {}

class DocumentResponse(BaseModel):
    success: bool
    document_id: Optional[str] = None
    message: str

class SearchResult(BaseModel):
    content: str
    score: float
    metadata: dict

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
