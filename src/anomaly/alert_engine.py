"""
Intelligent Alert Evaluation Engine for Energy Prediction & Optimization System.
Evaluates 10 real-time alert rules, persists alerts to PostgreSQL, and triggers critical email notifications.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any
from src.config.config import (
    HIGH_ENERGY_THRESHOLD, PEAK_DEMAND_THRESHOLD, HIGH_EQUIPMENT_LOAD,
    HIGH_CARBON_THRESHOLD, HIGH_COST_THRESHOLD, HIGH_TEMP_THRESHOLD,
    HIGH_OCCUPANCY_THRESHOLD, LOW_SOLAR_THRESHOLD
)
from src.database.db_connection import SessionLocal
from src.database.models import AlertRecord
from src.utils.logger import logger

def evaluate_alerts(reading: Dict[str, Any], anomaly_flag: int = 1) -> List[Dict[str, Any]]:
    """
    Evaluates real-time reading data against 10 alert criteria.
    Saves generated alerts to PostgreSQL database.
    Returns list of alert dictionaries.
    """
    alerts = []
    building = reading.get("Building", "Main Campus")
    timestamp_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    energy_kwh = float(reading.get("Energy_kWh", reading.get("Predicted_Energy_kWh", 0.0)))
    temp = float(reading.get("Temperature", 25.0))
    equipment_load = float(reading.get("Equipment_Load", 0.5))
    occupancy = float(reading.get("Occupancy", 150))
    solar_output = float(reading.get("Solar_Output", 100.0))
    cost = float(reading.get("Cost", energy_kwh * 8.5))
    carbon = float(reading.get("Carbon_Emission", energy_kwh * 0.82))

    # 1. High Energy Consumption
    if energy_kwh > HIGH_ENERGY_THRESHOLD:
        alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": timestamp_str,
            "severity": "High",
            "building": building,
            "category": "High Energy Consumption",
            "message": f"Energy consumption in {building} reached {energy_kwh:.1f} kWh, exceeding threshold of {HIGH_ENERGY_THRESHOLD} kWh.",
            "recommended_action": "Reduce non-essential HVAC and lighting loads immediately.",
            "status": "Active",
            "acknowledged": False,
            "color": "#FFA500",
            "notification_icon": "⚡"
        })

    # 2. Peak Demand
    if energy_kwh > PEAK_DEMAND_THRESHOLD:
        alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": timestamp_str,
            "severity": "Critical",
            "building": building,
            "category": "Peak Demand",
            "message": f"CRITICAL: Peak electrical demand spiked to {energy_kwh:.1f} kWh in {building}.",
            "recommended_action": "Dispatch battery storage and activate emergency load-shedding protocol.",
            "status": "Active",
            "acknowledged": False,
            "color": "#FF4B4B",
            "notification_icon": "🚨"
        })

    # 3. Abnormal Equipment Load
    if equipment_load > HIGH_EQUIPMENT_LOAD:
        alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": timestamp_str,
            "severity": "High",
            "building": building,
            "category": "Abnormal Equipment Load",
            "message": f"Equipment load factor is critically high at {equipment_load * 100:.0f}%.",
            "recommended_action": "Inspect heavy lab machinery, server racks, and chiller pumps for overload.",
            "status": "Active",
            "acknowledged": False,
            "color": "#FFA500",
            "notification_icon": "⚙️"
        })

    # 4. High Carbon Emission
    if carbon > HIGH_CARBON_THRESHOLD:
        alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": timestamp_str,
            "severity": "Medium",
            "building": building,
            "category": "High Carbon Emission",
            "message": f"Carbon emissions estimated at {carbon:.1f} kg CO₂, crossing threshold of {HIGH_CARBON_THRESHOLD} kg.",
            "recommended_action": "Maximize campus solar generation mix and power down standby equipment.",
            "status": "Active",
            "acknowledged": False,
            "color": "#FFD700",
            "notification_icon": "🌱"
        })

    # 5. High Cost
    if cost > HIGH_COST_THRESHOLD:
        alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": timestamp_str,
            "severity": "Medium",
            "building": building,
            "category": "High Cost",
            "message": f"Hourly electricity expenditure spiked to ₹{cost:,.2f}.",
            "recommended_action": "Shift flexible lab processing loads to off-peak tariff hours.",
            "status": "Active",
            "acknowledged": False,
            "color": "#FFD700",
            "notification_icon": "💰"
        })

    # 6. Equipment Failure Probability
    if anomaly_flag == -1 and equipment_load > 0.8:
        alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": timestamp_str,
            "severity": "Critical",
            "building": building,
            "category": "Equipment Failure Probability",
            "message": f"CRITICAL: High probability of equipment breakdown detected in {building}.",
            "recommended_action": "Dispatch maintenance engineering team for immediate diagnosis.",
            "status": "Active",
            "acknowledged": False,
            "color": "#FF4B4B",
            "notification_icon": "🛠️"
        })

    # 7. Temperature Threshold
    if temp > HIGH_TEMP_THRESHOLD:
        alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": timestamp_str,
            "severity": "High",
            "building": building,
            "category": "Temperature Threshold Crossed",
            "message": f"Ambient temperature measured at {temp:.1f}°C, exceeding maximum operational baseline.",
            "recommended_action": "Optimize HVAC setpoints to 24°C to avoid chiller unit tripping.",
            "status": "Active",
            "acknowledged": False,
            "color": "#FFA500",
            "notification_icon": "🌡️"
        })

    # 8. Occupancy Overload
    if occupancy > HIGH_OCCUPANCY_THRESHOLD:
        alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": timestamp_str,
            "severity": "Medium",
            "building": building,
            "category": "Occupancy Overload",
            "message": f"Building occupancy reached {occupancy:.0f} persons.",
            "recommended_action": "Increase fresh air ventilation intake and monitor cooling capacity.",
            "status": "Active",
            "acknowledged": False,
            "color": "#FFD700",
            "notification_icon": "👥"
        })

    # 9. Solar Output Drop
    if solar_output < LOW_SOLAR_THRESHOLD and reading.get("Hour", 12) in range(8, 17):
        alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": timestamp_str,
            "severity": "Medium",
            "building": building,
            "category": "Solar Output Drop",
            "message": f"Rooftop solar generation dropped to {solar_output:.1f} kW during daylight hours.",
            "recommended_action": "Inspect solar inverter logs and rooftop PV panel cleanliness.",
            "status": "Active",
            "acknowledged": False,
            "color": "#1E90FF",
            "notification_icon": "📉"
        })

    # 10. Anomaly Detection
    if anomaly_flag == -1:
        alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": timestamp_str,
            "severity": "High",
            "building": building,
            "category": "Anomaly Detected",
            "message": f"Machine Learning Isolation Forest flagged anomalous energy consumption pattern in {building}.",
            "recommended_action": "Review meter telemetry and run diagnostic audit.",
            "status": "Active",
            "acknowledged": False,
            "color": "#FFA500",
            "notification_icon": "🚨"
        })

    # Persist generated alerts to DB
    if alerts:
        db = SessionLocal()
        try:
            for a in alerts:
                record = AlertRecord(
                    id=a["id"],
                    timestamp=datetime.strptime(a["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    severity=a["severity"],
                    building=a["building"],
                    category=a["category"],
                    message=a["message"],
                    recommended_action=a["recommended_action"],
                    status=a["status"],
                    acknowledged=a["acknowledged"],
                    color=a["color"],
                    notification_icon=a["notification_icon"]
                )
                db.add(record)
            db.commit()
            logger.info(f"Saved {len(alerts)} alerts to database.")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to persist alerts to database: {e}")
        finally:
            db.close()

    return alerts
