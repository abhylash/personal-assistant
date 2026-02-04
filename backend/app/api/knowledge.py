from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import KnowledgeDocument, DocumentResponse, SearchResponse, SearchResult
from app.services.pinecone_service import PineconeService

router = APIRouter()
pinecone_service = PineconeService()

@router.post("/knowledge", response_model=DocumentResponse)
async def add_document(document: KnowledgeDocument):
    """Add a document to the knowledge base"""
    try:
        document_id = pinecone_service.add_document(
            content=document.content,
            title=document.title,
            metadata=document.metadata
        )
        
        return DocumentResponse(
            success=True,
            document_id=document_id,
            message="Document added successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/knowledge/{document_id}", response_model=DocumentResponse)
async def delete_document(document_id: str):
    """Delete a document from the knowledge base"""
    try:
        success = pinecone_service.delete_document(document_id)
        
        if success:
            return DocumentResponse(
                success=True,
                document_id=document_id,
                message="Document deleted successfully"
            )
        else:
            return DocumentResponse(
                success=False,
                message="Failed to delete document"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/knowledge/search", response_model=SearchResponse)
async def search_knowledge(query: str, top_k: int = 5):
    """Search the knowledge base"""
    try:
        results = pinecone_service.search(query, top_k)
        
        search_results = [
            SearchResult(
                content=result["content"],
                score=result["score"],
                metadata=result["metadata"]
            )
            for result in results
        ]
        
        return SearchResponse(
            query=query,
            results=search_results
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/knowledge/stats")
async def get_knowledge_stats():
    """Get knowledge base statistics"""
    try:
        stats = pinecone_service.list_documents()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
