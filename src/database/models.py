"""
SQLAlchemy ORM Data Models for Energy Prediction & Optimization System.
Defines tables for Predictions, Alerts, Chat History, Reports, and Optimization Logs.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, JSON
from src.database.db_connection import Base

def utc_now():
    return datetime.now(timezone.utc)

class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=utc_now, index=True)
    building = Column(String(100), nullable=False, index=True)
    building_type = Column(String(100), nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    hour = Column(Integer, nullable=True)
    day = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)
    weekend = Column(Integer, nullable=True)
    holiday = Column(Integer, nullable=True)
    equipment_load = Column(Float, nullable=True)
    predicted_energy_kwh = Column(Float, nullable=False)
    confidence_score = Column(Float, default=0.95)
    created_at = Column(DateTime, default=utc_now)

class AlertRecord(Base):
    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=utc_now, index=True)
    severity = Column(String(20), nullable=False, index=True)  # Critical, High, Medium, Low
    building = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False)  # High Energy, Peak Demand, Anomaly, etc.
    message = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=False)
    status = Column(String(20), default="Active")  # Active, Acknowledged, Resolved
    acknowledged = Column(Boolean, default=False)
    color = Column(String(20), default="#FF4B4B")
    notification_icon = Column(String(10), default="🚨")

class ChatRecord(Base):
    __tablename__ = "chat_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=utc_now, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    confidence_score = Column(Float, default=0.90)
    sources = Column(JSON, nullable=True)

class ReportRecord(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=utc_now, index=True)
    report_title = Column(String(200), nullable=False)
    format = Column(String(20), nullable=False)  # PDF, DOCX, MD
    file_path = Column(Text, nullable=False)
    summary_text = Column(Text, nullable=True)

class OptimizationLogRecord(Base):
    __tablename__ = "optimization_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=utc_now, index=True)
    building = Column(String(100), nullable=True)
    potential_savings_kwh = Column(Float, nullable=False)
    cost_savings_inr = Column(Float, nullable=False)
    carbon_reduction_kg = Column(Float, nullable=False)
    recommendations_count = Column(Integer, default=0)
