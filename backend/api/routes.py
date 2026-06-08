# backend/api/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.core.agent import run_jarvis_task

router = APIRouter()

class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    status: str
    reply: str

# Changed from 'async def' to standard 'def' so blocking terminal actions don't crash the event loop
@router.post("/execute", response_model=CommandResponse)
def execute_command(req: CommandRequest):
    """
    Receives text from the frontend interface, hands it off to the 
    Open Interpreter agent, and returns the final system response.
    """
    try:
        # Hand off the command to the autonomous agent
        final_reply = run_jarvis_task(req.command)
        
        return CommandResponse(status="success", reply=str(final_reply))
        
    except Exception as e:
        return CommandResponse(status="error", reply=f"Agent Malfunction: {str(e)}")