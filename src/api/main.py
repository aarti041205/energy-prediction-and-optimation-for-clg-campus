"""
Main Entry Point Alias for FastAPI Application.
Imports production app instance from src.api.app.
"""

from src.api.app import app

__all__ = ["app"]