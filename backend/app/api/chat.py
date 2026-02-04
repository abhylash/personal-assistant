from fastapi import APIRouter, HTTPException
from typing import List
import uuid

from app.models.schemas import ChatMessage, ChatResponse, SearchResult
from app.services.pinecone_service import PineconeService
from app.services.llm_service import LLMService

router = APIRouter()
pinecone_service = PineconeService()
llm_service = LLMService()

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Handle chat messages"""
    try:
        # Generate or use existing session ID
        session_id = message.session_id or str(uuid.uuid4())
        
        # Search knowledge base for relevant context
        search_results = pinecone_service.search(message.message, top_k=3)
        
        # Generate response using LLM
        response = llm_service.generate_response(message.message, search_results)
        
        # Extract sources
        sources = [result["metadata"].get("title", "Unknown") for result in search_results]
        
        return ChatResponse(
            response=response,
            sources=sources,
            session_id=session_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/sessions/{session_id}")
async def get_session_history(session_id: str):
    """Get chat history for a session (placeholder)"""
    return {"session_id": session_id, "messages": []}
