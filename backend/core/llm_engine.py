# backend/core/llm_engine.py
import httpx
from backend.core.config import settings

async def generate_response(prompt: str, model: str = settings.DEFAULT_MODEL) -> str:
    """
    Sends a prompt to the local Ollama instance asynchronously.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False # Set to True later if you want streaming text in your UI
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # 60-second timeout allows the local GPU/CPU time to generate the response
            response = await client.post(
                settings.OLLAMA_BASE_URL, 
                json=payload, 
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            
            return data.get("response", "Error: No response generated.")
            
        except Exception as e:
            return f"System Malfunction: {str(e)}"