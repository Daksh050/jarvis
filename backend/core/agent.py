# backend/core/agent.py
from interpreter import interpreter
import os

# 1. Secure Workspace Configuration
WORKSPACE_DIR = os.path.abspath(os.path.join(os.getcwd(), "data", "workspace"))
os.makedirs(WORKSPACE_DIR, exist_ok=True) 

# 2. Initialize Agent Core
interpreter.offline = True
interpreter.llm.model = "ollama/llama3"
interpreter.llm.api_base = "http://localhost:11434"

# 3. Configure the Sandbox (Requires terminal 'y' to run code)
interpreter.auto_run = False 

# 4. The Master Directives (Workspace + Conversational Bypass)
# 4. The Master Directives (Workspace + Conversational Bypass + Real-Time Data)
custom_instructions = f"""
CRITICAL SECURITY RULE: Your ONLY allowed workspace directory is EXACTLY this path:
{WORKSPACE_DIR}
When asked to save a file, you MUST use this exact absolute path. Do NOT make up paths. Combine this exact path with the requested filename before saving.

CONVERSATIONAL BYPASS RULE: If the user asks for advice, brainstorming, name suggestions, or conversational drafting, reply DIRECTLY with text. Do NOT write, plan, or execute Python code unless a physical task, file operation, or data calculation is explicitly required.

REAL-TIME DATA RULE: If the user asks for the weather without specifying a location, default to checking Hinjavadi, Maharashtra. Do NOT use OpenWeatherMap. Write a quick Python script using the 'requests' library to fetch text data from 'https://wttr.in/Hinjavadi?format=3' (or replace 'Hinjavadi' with the requested city) and return the output directly.
"""
interpreter.system_message += custom_instructions
def run_jarvis_task(user_command: str) -> str:
    """Passes the user command to the AI and returns the final text response."""
    response = interpreter.chat(user_command)
    
    if isinstance(response, list) and len(response) > 0:
        last_message = response[-1].get("content")
        if last_message:
             return last_message
             
    return "Task execution completed. Check terminal for specific output logs."