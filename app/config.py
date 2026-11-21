"""
PranaAI Configuration Module.

Manages application settings, environment variables, security flags,
and Google Gemini GenAI credentials adhering strictly to the Zero-Secret Law.
"""

import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()


class AppConfig(BaseModel):
    """Configuration settings for PranaAI."""
    
    app_name: str = "PranaAI (प्राण AI) — Urban Air Quality & Smog Assistant"
    app_version: str = "1.0.0"
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "production"))
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    
    # Port & Host
    host: str = Field(default_factory=lambda: os.getenv("HOST", "0.0.0.0"))
    port: int = Field(default_factory=lambda: int(os.getenv("PORT", "8000")))
    
    # Gemini API Credentials (Zero-Secret Law: Never hardcoded)
    gemini_api_key: str = Field(
        default_factory=lambda: os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
    )
    gemini_model: str = Field(
        default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    )
    
    # Security & CORS
    allowed_origins: list[str] = ["*"]
    
    # Offline Fallback Guarantee
    allow_deterministic_fallback: bool = True


config = AppConfig()
