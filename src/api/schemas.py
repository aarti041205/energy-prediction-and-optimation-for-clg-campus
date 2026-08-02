"""
Pydantic Data Validation Schemas for FastAPI Endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PredictionRequest(BaseModel):
    Building: str = Field(default="AI Lab", description="Name of campus building")
    Building_Type: str = Field(default="Laboratory", description="Type of building")
    Temperature: float = Field(default=28.0, ge=-10.0, le=60.0, description="Ambient temperature (°C)")
    Humidity: float = Field(default=65.0, ge=0.0, le=100.0, description="Relative humidity (%)")
    Hour: int = Field(default=14, ge=0, le=23, description="Hour of the day (0-23)")
    Day: int = Field(default=15, ge=1, le=31, description="Day of the month (1-31)")
    Month: int = Field(default=8, ge=1, le=12, description="Month of the year (1-12)")
    Weekend: int = Field(default=0, ge=0, le=1, description="Is weekend flag (0 or 1)")
    Holiday: int = Field(default=0, ge=0, le=1, description="Is holiday flag (0 or 1)")
    Equipment_Load: float = Field(default=0.85, ge=0.0, le=1.0, description="Equipment load ratio (0.0 - 1.0)")
    Occupancy: Optional[int] = Field(default=180, ge=0, description="Building occupancy count")
    Solar_Output: Optional[float] = Field(default=120.0, ge=0.0, description="Solar power generation (kW)")

class PredictionResponse(BaseModel):
    id: str
    building: str
    predicted_energy_kwh: float
    confidence_score: float
    timestamp: str
    electricity_cost_inr: float
    carbon_emission_kg: float
    alerts_triggered: List[Dict[str, Any]]

class ChatRequest(BaseModel):
    question: str = Field(..., description="User query for RAG chatbot")
    history: Optional[List[Dict[str, str]]] = Field(default=[], description="Chat history context")

class ChatResponse(BaseModel):
    question: str
    answer: str
    confidence: float
    top_chunks_retrieved: int
    sources: List[Dict[str, Any]]

class OptimizationRequest(BaseModel):
    Building: Optional[str] = Field(default="Main Campus")
    Energy_kWh: Optional[float] = Field(default=350.0)

class AnomalyRequest(BaseModel):
    Building: str = Field(default="Library")
    Building_Type: str = Field(default="Academic")
    Temperature: float = Field(default=32.0)
    Humidity: float = Field(default=70.0)
    Equipment_Load: float = Field(default=0.90)
    Actual_Energy_kWh: float = Field(default=480.0)

class ReportRequest(BaseModel):
    report_type: Optional[str] = Field(default="Executive")
    format: Optional[str] = Field(default="PDF")  # PDF, DOCX, MD