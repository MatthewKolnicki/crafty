"""
Configuration management for Crafty CRM.

This module handles environment variable loading with proper fallbacks,
error handling, and environment-specific configuration.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Application configuration with environment variable management."""

    def __init__(self):
        self._load_environment()
        self._validate_config()

    def _load_environment(self):
        """Load environment variables with proper fallbacks."""
        # Try to load from .env file first (for local development)
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)
        else:
            # Fallback to .sample_env for development
            sample_env_file = Path(".sample_env")
            if sample_env_file.exists():
                load_dotenv(sample_env_file)
            else:
                # In production, rely on system environment variables
                print(
                    "No .env or .sample_env file found. Using system environment variables."
                )

    def _validate_config(self):
        """Validate that required configuration is present."""
        required_vars = ["POSTGRES_PASSWORD"]
        missing_vars = [var for var in required_vars if not self.get(var)]

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable with optional default."""
        return os.getenv(key, default)

    @property
    def database_config(self) -> dict:
        """Get database configuration."""
        return {
            "host": self.get("POSTGRES_HOST", "localhost"),
            "port": self.get("POSTGRES_PORT", "5432"),
            "user": self.get("POSTGRES_USER", "postgres"),
            "password": self.get("POSTGRES_PASSWORD"),
            "database": self.get("POSTGRES_DB", "crafty"),
        }

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.get("ENVIRONMENT", "development").lower() == "production"

    @property
    def debug(self) -> bool:
        """Check if debug mode is enabled."""
        return not self.is_production and self.get("DEBUG", "true").lower() == "true"


# Global configuration instance
config = Config()
