import pinecone
from typing import List, Dict, Any
import uuid
from sentence_transformers import SentenceTransformer
import numpy as np
from app.core.config import settings

class PineconeService:
    def __init__(self):
        self.index_name = settings.pinecone_index_name
        self.demo_mode = settings.pinecone_api_key == "demo_key_please_replace"
        
        if not self.demo_mode:
            try:
                pinecone.init(
                    api_key=settings.pinecone_api_key,
                    environment=settings.pinecone_environment
                )
                
                # Initialize embedding model
                self.embedding_model = SentenceTransformer(settings.embedding_model)
                
                # Create index if it doesn't exist
                if self.index_name not in pinecone.list_indexes():
                    pinecone.create_index(
                        name=self.index_name,
                        dimension=384,  # Dimension for all-MiniLM-L6-v2
                        metric="cosine"
                    )
                
                self.index = pinecone.Index(self.index_name)
            except Exception as e:
                print(f"Pinecone initialization failed: {e}")
                self.demo_mode = True
                self.index = None
        else:
            print("Running in demo mode - Pinecone operations will be simulated")
            self.index = None
            self.embedding_model = SentenceTransformer(settings.embedding_model)
    
    def add_document(self, content: str, title: str = None, metadata: Dict = None) -> str:
        """Add a document to the vector database"""
        document_id = str(uuid.uuid4())
        
        if self.demo_mode:
            print(f"[DEMO] Would add document: {title or 'Untitled'}")
            return document_id
        
        # Generate embeddings
        embedding = self.embedding_model.encode([content])[0].tolist()
        
        # Prepare metadata
        doc_metadata = {
            "content": content,
            "title": title or f"Document {document_id[:8]}",
            "document_id": document_id,
            **(metadata or {})
        }
        
        # Upsert to Pinecone
        self.index.upsert(
            vectors=[{
                "id": document_id,
                "values": embedding,
                "metadata": doc_metadata
            }]
        )
        
        return document_id
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        if self.demo_mode:
            print(f"[DEMO] Would search for: {query}")
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Search in Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Format results
        formatted_results = []
        for match in results.get("matches", []):
            formatted_results.append({
                "content": match["metadata"]["content"],
                "score": match["score"],
                "metadata": match["metadata"]
            })
        
        return formatted_results
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document from the vector database"""
        if self.demo_mode:
            print(f"[DEMO] Would delete document: {document_id}")
            return True
            
        try:
            self.index.delete(ids=[document_id])
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in the index"""
        if self.demo_mode:
            return {"total_vectors": 0}
            
        try:
            stats = self.index.describe_index_stats()
            return {"total_vectors": stats["total_vector_count"]}
        except Exception as e:
            print(f"Error listing documents: {e}")
            return []
