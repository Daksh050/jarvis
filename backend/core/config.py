# backend/core/config.py

class Settings:
    PROJECT_NAME = "Local_JARVIS"
    OLLAMA_BASE_URL = "http://localhost:11434"
    
    # Define the models you pulled earlier
    DEFAULT_MODEL = "llama3"
    CODER_MODEL = "codellama"

settings = Settings()