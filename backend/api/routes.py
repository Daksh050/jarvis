# backend/api/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.llm_engine import generate_response

router = APIRouter()

# Data models for strict type checking
class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    status: str
    reply: str

@router.post("/execute", response_model=CommandResponse)
async def execute_command(req: CommandRequest):
    """
    Receives text from the frontend, processes it via the local LLM,
    and returns the system response.
    """
    # System prompt to give the AI its persona and constraints
    system_prompt = f"You are a highly efficient local assistant named Jarvis. Be concise. User command: {req.command}"
    
    # Await the response from our core engine
    reply = await generate_response(system_prompt)
    
    # In the future, we will add an "Intent Parser" here to trigger 
    # specific scripts in backend/skills/ instead of just talking back.
    
    return CommandResponse(status="success", reply=reply)