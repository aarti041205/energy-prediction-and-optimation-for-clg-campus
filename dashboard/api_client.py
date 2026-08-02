"""
API Client Helper for Streamlit Dashboard.
Encapsulates HTTP requests to FastAPI backend with timeout, error handling, loading states, and fallback logic.
"""

import os
import requests
from typing import Dict, Any, Optional

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def get_api_health() -> Dict[str, Any]:
    """Checks FastAPI server health status."""
    try:
        res = requests.get(f"{API_BASE_URL}/health", timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return {"status": "offline", "model_loaded": False, "database_connected": False}

def post_prediction(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Posts prediction request to FastAPI /predict endpoint."""
    try:
        res = requests.post(f"{API_BASE_URL}/predict", json=payload, timeout=8)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "error": f"API Error ({res.status_code}): {res.text}"}
    except Exception as e:
        return {"success": False, "error": f"Connection Failed: Cannot reach FastAPI server at {API_BASE_URL}. Ensure backend is running."}

def post_chat(question: str, history: list = None) -> Dict[str, Any]:
    """Posts chat prompt to FastAPI /chat endpoint."""
    try:
        res = requests.post(f"{API_BASE_URL}/chat", json={"question": question, "history": history or []}, timeout=15)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "error": f"RAG Chat Error ({res.status_code}): {res.text}"}
    except Exception as e:
        return {"success": False, "error": f"Connection Failed: {e}"}

def get_analytics_data(building: str = "All") -> Dict[str, Any]:
    """Fetches analytics data from FastAPI /analytics endpoint."""
    try:
        params = {"building": building} if building and building != "All" else {}
        res = requests.get(f"{API_BASE_URL}/analytics", params=params, timeout=8)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "error": f"Analytics API Error ({res.status_code})"}
    except Exception as e:
        return {"success": False, "error": f"Connection Failed: {e}"}

def post_optimization(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Fetches optimization recommendations from FastAPI /optimize endpoint."""
    try:
        res = requests.post(f"{API_BASE_URL}/optimize", json=payload, timeout=8)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "error": f"Optimization API Error ({res.status_code})"}
    except Exception as e:
        return {"success": False, "error": f"Connection Failed: {e}"}

def post_anomaly(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Posts anomaly check request to FastAPI /anomaly endpoint."""
    try:
        res = requests.post(f"{API_BASE_URL}/anomaly", json=payload, timeout=8)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "error": f"Anomaly API Error ({res.status_code})"}
    except Exception as e:
        return {"success": False, "error": f"Connection Failed: {e}"}

def get_alerts_data(severity: str = None, building: str = None) -> list:
    """Fetches system alerts from FastAPI /alerts endpoint."""
    try:
        params = {}
        if severity and severity != "All":
            params["severity"] = severity
        if building and building != "All":
            params["building"] = building
        res = requests.get(f"{API_BASE_URL}/alerts", params=params, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []

def post_acknowledge_alert(alert_id: str) -> bool:
    """Acknowledges an alert via FastAPI endpoint."""
    try:
        res = requests.post(f"{API_BASE_URL}/alerts/{alert_id}/acknowledge", timeout=5)
        return res.status_code == 200
    except Exception:
        return False

def post_generate_report() -> Dict[str, Any]:
    """Triggers AI Report Generation via FastAPI /generate-report endpoint."""
    try:
        res = requests.post(f"{API_BASE_URL}/generate-report", json={}, timeout=25)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        return {"success": False, "error": f"Report API Error ({res.status_code})"}
    except Exception as e:
        return {"success": False, "error": f"Connection Failed: {e}"}
