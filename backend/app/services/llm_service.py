import openai
import requests
from typing import List, Dict, Any
from app.core.config import settings
from app.models.schemas import SearchResult

class LLMService:
    def __init__(self):
        self.demo_mode = settings.openai_api_key == "demo_key_please_replace"
        if not self.demo_mode and settings.openai_api_key:
            openai.api_key = settings.openai_api_key
        self.llm_api_url = settings.llm_api_url
        self.llm_api_key = settings.llm_api_key
    
    def generate_response(self, query: str, context: List[SearchResult] = None) -> str:
        """Generate a response using the LLM with context from knowledge base"""
        
        if self.demo_mode:
            return f"[DEMO MODE] I received your question: '{query}'. In production, I would provide a detailed response using either your self-hosted LLM or OpenAI. Please configure your API keys in the .env file to enable full functionality."
        
        # Prepare context from search results
        context_text = ""
        if context:
            context_text = "\n".join([
                f"Context {i+1}: {result.content[:500]}..." 
                for i, result in enumerate(context)
            ])
        
        # Create prompt
        if context_text:
            prompt = f"""You are a helpful AI assistant. Use the following context to answer the user's question. 
If the context doesn't contain relevant information, use your general knowledge.

Context:
{context_text}

User Question: {query}

Provide a helpful and accurate response:"""
        else:
            prompt = f"""You are a helpful AI assistant. Answer the user's question to the best of your ability.

User Question: {query}

Provide a helpful and accurate response:"""
        
        # Try self-hosted LLM first
        if self.llm_api_url:
            try:
                return self._call_self_hosted_llm(prompt)
            except Exception as e:
                print(f"Self-hosted LLM failed: {e}")
        
        # Fallback to OpenAI
        if not self.demo_mode and settings.openai_api_key:
            try:
                return self._call_openai(prompt)
            except Exception as e:
                print(f"OpenAI failed: {e}")
        
        return "I apologize, but I'm currently unable to process your request. Please check your LLM configuration."
    
    def _call_self_hosted_llm(self, prompt: str) -> str:
        """Call self-hosted LLM API"""
        headers = {
            "Content-Type": "application/json",
        }
        
        if self.llm_api_key:
            headers["Authorization"] = f"Bearer {self.llm_api_key}"
        
        data = {
            "prompt": prompt,
            "max_tokens": 500,
            "temperature": 0.7,
        }
        
        response = requests.post(
            f"{self.llm_api_url}/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Handle different response formats
        if "choices" in result:
            return result["choices"][0]["text"].strip()
        elif "response" in result:
            return result["response"].strip()
        else:
            raise ValueError("Unexpected response format from LLM")
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        
        return response.choices[0].message.content.strip()
