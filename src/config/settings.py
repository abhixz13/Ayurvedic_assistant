"""
Configuration settings for the Ayurvedic Diagnostic Assistant.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Configuration settings for the Ayurvedic Diagnostic Assistant."""
    
    def __init__(self):
        # Google AI API Configuration
        self.google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Model Configuration
        self.model_name: str = os.getenv("MODEL_NAME", "gemini-2.0-flash-exp")
        self.temperature: float = float(os.getenv("TEMPERATURE", "0.2"))
        self.max_tokens: int = int(os.getenv("MAX_TOKENS", "4096"))
        
        # RAG Configuration
        self.embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
        self.chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
        self.top_k_retrieval: int = int(os.getenv("TOP_K_RETRIEVAL", "5"))
        
        # Vector Store Configuration
        self.vector_store_path: str = os.getenv("VECTOR_STORE_PATH", "./data/processed/vector_store")
        self.use_gpu: bool = os.getenv("USE_GPU", "false").lower() == "true"
        
        # Document Processing
        self.supported_formats: list = os.getenv("SUPPORTED_FORMATS", "pdf,docx,txt").split(",")
        self.max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
        
        # UI Configuration
        self.display_mode: str = os.getenv("DISPLAY_MODE", "html")
        self.enable_interactive: bool = os.getenv("ENABLE_INTERACTIVE", "true").lower() == "true"
        
        # Paths
        self.data_raw_path: str = "./data/raw"
        self.data_processed_path: str = "./data/processed"
        
    def validate(self) -> bool:
        """Validate configuration settings."""
        if not self.google_api_key:
            return False
        if self.temperature < 0 or self.temperature > 1:
            return False
        if self.chunk_size <= 0:
            return False
        if self.top_k_retrieval <= 0:
            return False
        return True
    
    def get_model_config(self) -> dict:
        """Get model configuration dictionary."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    def get_rag_config(self) -> dict:
        """Get RAG configuration dictionary."""
        return {
            "embedding_model": self.embedding_model,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "top_k_retrieval": self.top_k_retrieval,
            "vector_store_path": self.vector_store_path,
            "use_gpu": self.use_gpu
        }


# Global settings instance
settings = Settings() 