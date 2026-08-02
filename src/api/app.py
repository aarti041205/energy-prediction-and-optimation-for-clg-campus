"""
FastAPI REST Application for Energy Prediction & Optimization System.
Provides endpoints for Predictions, RAG Chatbot, Analytics, Optimization, Alerts, Anomaly Detection, AI Reports, and Exports.
"""

import os
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query, Response
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.api.schemas import (
    PredictionRequest, PredictionResponse, ChatRequest, ChatResponse,
    OptimizationRequest, AnomalyRequest, ReportRequest
)
from src.api.predictor import get_model_manager, predict_energy_with_meta
from src.rag.chatbot import ask
from src.optimization.recommendations import generate_comprehensive_optimization
from src.utils.report_generator import generate_and_export_report
from src.database.db_connection import get_db, init_db, check_db_connection
from src.database.models import PredictionRecord, AlertRecord, ChatRecord, ReportRecord
from src.utils.logger import logger
from src.config.config import BASE_DIR, PROCESSED_DATA, PROCESSED_ALT_DATA, REPORTS_DIR

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler: loads ML models and initializes database ONCE during startup."""
    logger.info("Starting up FastAPI application...")
    manager = get_model_manager()
    manager.load_models()
    init_db()
    yield
    logger.info("Shutting down FastAPI application...")

app = FastAPI(
    title="Campus Energy Prediction & Optimization System API",
    description="Production REST API powered by Machine Learning, GenAI RAG, and PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan
)

from fastapi.staticfiles import StaticFiles

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Frontend UI static files
frontend_dir = BASE_DIR / "frontend"
if frontend_dir.exists():
    app.mount("/dashboard-ui", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


# ---------------------------------------------------------
# 1. Health & Home Endpoints
# ---------------------------------------------------------

@app.get("/")
def home():
    return {
        "status": "online",
        "system": "Campus Energy Prediction & Optimization System API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "dashboard_ui": "/dashboard-ui"
    }

@app.get("/health")
def health_check():
    manager = get_model_manager()
    db_ok = check_db_connection()
    return {
        "status": "healthy" if db_ok else "degraded",
        "model_loaded": manager.rf_model is not None,
        "anomaly_model_loaded": manager.anomaly_model is not None,
        "database_connected": db_ok,
        "vector_db_ready": (REPORTS_DIR.parent / "vector_db" / "index.faiss").exists()
    }

# ---------------------------------------------------------
# 2. Prediction API
# ---------------------------------------------------------

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest, background_tasks: BackgroundTasks):
    try:
        req_dict = request.model_dump() if hasattr(request, "model_dump") else request.dict()
        result = predict_energy_with_meta(req_dict, background_tasks=background_tasks)
        return result
    except Exception as e:
        logger.error(f"Prediction API endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/prediction-history")
def prediction_history(limit: int = 50, db: Session = Depends(get_db)):
    try:
        records = db.query(PredictionRecord).order_by(PredictionRecord.timestamp.desc()).limit(limit).all()
        return [
            {
                "id": r.id,
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "building": r.building,
                "building_type": r.building_type,
                "predicted_energy_kwh": r.predicted_energy_kwh,
                "confidence_score": r.confidence_score
            }
            for r in records
        ]
    except Exception as e:
        logger.error(f"Failed to fetch prediction history: {e}")
        return []

# ---------------------------------------------------------
# 3. RAG Chatbot API
# ---------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = ask(request.question, history=request.history)
        return result
    except Exception as e:
        logger.error(f"RAG Chat API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# 4. Analytics API
# ---------------------------------------------------------

@app.get("/analytics")
def get_analytics(building: Optional[str] = Query(None)):
    data_file = PROCESSED_DATA if PROCESSED_DATA.exists() else PROCESSED_ALT_DATA
    if not data_file.exists():
        # Fallback mock analytics
        return {
            "total_energy": 1250000.0,
            "avg_energy": 285.4,
            "max_demand": 540.0,
            "total_cost": 10625000.0,
            "total_carbon": 1025.0,
            "building_breakdown": [
                {"Building": "AI Lab", "Energy_kWh": 450000.0, "Cost": 3825000.0, "Carbon": 369.0},
                {"Building": "Library", "Energy_kWh": 290000.0, "Cost": 2465000.0, "Carbon": 237.8},
                {"Building": "Hostel", "Energy_kWh": 510000.0, "Cost": 4335000.0, "Carbon": 418.2}
            ],
            "monthly_trend": [
                {"Month": m, "Energy_kWh": 100000 + m * 5000} for m in range(1, 13)
            ]
        }

    try:
        df = pd.read_csv(data_file)
        if building and building != "All":
            df = df[df["Building"] == building]

        energy_col = "Energy_kWh" if "Energy_kWh" in df.columns else ("Energy_Consumption" if "Energy_Consumption" in df.columns else df.columns[0])
        cost_col = "Cost" if "Cost" in df.columns else None
        carbon_col = "Carbon_Emission" if "Carbon_Emission" in df.columns else None

        total_energy = float(df[energy_col].sum())
        avg_energy = float(df[energy_col].mean())
        max_demand = float(df[energy_col].max())
        total_cost = float(df[cost_col].sum()) if cost_col else total_energy * 8.5
        total_carbon = float(df[carbon_col].sum()) if carbon_col else total_energy * 0.82 / 1000.0

        building_breakdown = df.groupby("Building")[energy_col].sum().reset_index().to_dict(orient="records") if "Building" in df.columns else []
        monthly_trend = df.groupby("Month")[energy_col].mean().reset_index().to_dict(orient="records") if "Month" in df.columns else []

        return {
            "total_energy": round(total_energy, 2),
            "avg_energy": round(avg_energy, 2),
            "max_demand": round(max_demand, 2),
            "total_cost": round(total_cost, 2),
            "total_carbon": round(total_carbon, 2),
            "building_breakdown": building_breakdown,
            "monthly_trend": monthly_trend
        }
    except Exception as e:
        logger.error(f"Analytics computation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# 5. Optimization & Anomaly Endpoints
# ---------------------------------------------------------

@app.post("/optimize")
def optimize(request: OptimizationRequest):
    try:
        req_dict = request.model_dump() if hasattr(request, "model_dump") else request.dict()
        return generate_comprehensive_optimization(req_dict)
    except Exception as e:
        logger.error(f"Optimization API error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/anomaly")
def detect_anomaly(request: AnomalyRequest):
    manager = get_model_manager()
    building = request.Building
    actual = request.Actual_Energy_kWh

    predicted = 280.0
    if manager.rf_model is not None:
        try:
            df_in = pd.DataFrame([{
                "Building": building,
                "Building_Type": request.Building_Type,
                "Temperature": request.Temperature,
                "Humidity": request.Humidity,
                "Hour": 14,
                "Day": 15,
                "Month": 8,
                "Weekend": 0,
                "Holiday": 0,
                "Equipment_Load": request.Equipment_Load
            }])
            predicted = float(manager.rf_model.predict(df_in)[0])
        except Exception:
            predicted = 280.0

    diff = abs(actual - predicted)
    is_anomaly = diff > 35.0

    return {
        "building": building,
        "actual_energy_kwh": round(actual, 2),
        "predicted_energy_kwh": round(predicted, 2),
        "difference_kwh": round(diff, 2),
        "is_anomaly": is_anomaly,
        "anomaly_score": round(diff / max(predicted, 1.0), 3),
        "recommendation": "Inspect chiller valve and meter calibration" if is_anomaly else "Normal operation"
    }

# ---------------------------------------------------------
# 6. Intelligent Alerts API
# ---------------------------------------------------------

@app.get("/alerts")
def get_alerts(
    severity: Optional[str] = None,
    building: Optional[str] = None,
    acknowledged: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(AlertRecord)
        if severity:
            query = query.filter(AlertRecord.severity == severity)
        if building:
            query = query.filter(AlertRecord.building == building)
        if acknowledged is not None:
            query = query.filter(AlertRecord.acknowledged == acknowledged)

        records = query.order_by(AlertRecord.timestamp.desc()).limit(100).all()
        return [
            {
                "id": r.id,
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "severity": r.severity,
                "building": r.building,
                "category": r.category,
                "message": r.message,
                "recommended_action": r.recommended_action,
                "status": r.status,
                "acknowledged": r.acknowledged,
                "color": r.color,
                "notification_icon": r.notification_icon
            }
            for r in records
        ]
    except Exception as e:
        logger.error(f"Error querying alerts: {e}")
        return []

@app.post("/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str, db: Session = Depends(get_db)):
    try:
        record = db.query(AlertRecord).filter(AlertRecord.id == alert_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Alert ID not found")
        record.acknowledged = True
        record.status = "Acknowledged"
        db.commit()
        return {"status": "success", "alert_id": alert_id, "acknowledged": True}
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# 7. AI Report & File Downloads API
# ---------------------------------------------------------

@app.post("/generate-report")
def generate_report(request: ReportRequest):
    try:
        content, md_path, pdf_path, docx_path = generate_and_export_report()
        return {
            "status": "success",
            "report_summary": content[:400] + "...",
            "pdf_url": f"/download-report?filename={os.path.basename(pdf_path)}",
            "docx_url": f"/download-report?filename={os.path.basename(docx_path)}",
            "md_url": f"/download-report?filename={os.path.basename(md_path)}"
        }
    except Exception as e:
        logger.error(f"Report generation endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-report")
def download_report(filename: str):
    file_path = REPORTS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=str(file_path), filename=filename)

@app.get("/export-csv")
def export_csv(type: str = "analytics"):
    try:
        data_file = PROCESSED_DATA if PROCESSED_DATA.exists() else PROCESSED_ALT_DATA
        if type == "optimization" and (REPORTS_DIR / "optimization_report.csv").exists():
            data_file = REPORTS_DIR / "optimization_report.csv"
        elif type == "anomalies" and (REPORTS_DIR / "only_anomalies.csv").exists():
            data_file = REPORTS_DIR / "only_anomalies.csv"

        df = pd.read_csv(data_file)
        csv_data = df.to_csv(index=False)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={type}_export.csv"}
        )
    except Exception as e:
        logger.error(f"CSV export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export-excel")
def export_excel(type: str = "analytics"):
    try:
        data_file = PROCESSED_DATA if PROCESSED_DATA.exists() else PROCESSED_ALT_DATA
        df = pd.read_csv(data_file)
        out_path = REPORTS_DIR / f"{type}_export.xlsx"
        df.to_excel(out_path, index=False)
        return FileResponse(path=str(out_path), filename=f"{type}_export.xlsx")
    except Exception as e:
        logger.error(f"Excel export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))