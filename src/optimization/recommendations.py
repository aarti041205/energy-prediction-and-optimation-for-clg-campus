"""
Energy Optimization Recommendation Engine.
Calculates energy savings, financial impact, carbon reduction, peak load shifting strategies, 
HVAC/Lighting/Equipment/Solar/Battery optimization, recommendation priorities, and annual projections.
"""

import os
from typing import Dict, Any, List
import pandas as pd
from src.config.config import PRICE_PER_KWH, CARBON_PER_KWH, REPORTS_DIR
from src.utils.logger import logger

def generate_comprehensive_optimization(data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generates actionable optimization recommendations covering all 9 system categories.
    Returns structured dict with recommendations breakdown and financial metrics.
    """
    building = data.get("Building", "Main Campus") if data else "Main Campus"
    current_energy = float(data.get("Energy_kWh", 350.0)) if data else 350.0

    # 1. HVAC Optimization
    hvac_saving_pct = 14.5
    hvac_kwh = current_energy * (hvac_saving_pct / 100.0)
    hvac_cost = hvac_kwh * PRICE_PER_KWH
    hvac_carbon = hvac_kwh * CARBON_PER_KWH

    # 2. Lighting Optimization
    lighting_saving_pct = 8.0
    lighting_kwh = current_energy * (lighting_saving_pct / 100.0)
    lighting_cost = lighting_kwh * PRICE_PER_KWH
    lighting_carbon = lighting_kwh * CARBON_PER_KWH

    # 3. Equipment Scheduling
    equip_saving_pct = 10.0
    equip_kwh = current_energy * (equip_saving_pct / 100.0)
    equip_cost = equip_kwh * PRICE_PER_KWH
    equip_carbon = equip_kwh * CARBON_PER_KWH

    # 4. Peak Shifting
    peak_shift_kwh = current_energy * 0.12

    # 5. Solar Utilization
    solar_utilization_kw = 140.0

    # 6. Battery Utilization
    battery_utilization_kwh = 85.0

    total_kwh_saved = hvac_kwh + lighting_kwh + equip_kwh + (peak_shift_kwh * 0.5)
    total_cost_saved = total_kwh_saved * PRICE_PER_KWH
    total_carbon_reduced = total_kwh_saved * CARBON_PER_KWH
    expected_annual_savings = total_cost_saved * 24 * 365 * 0.45  # weighted average load

    recommendations_list = [
        {
            "category": "HVAC Optimization",
            "recommendation": f"Adjust chilled water temperature to 7°C and set indoor thermostats to 24°C in {building}.",
            "energy_saving_pct": hvac_saving_pct,
            "estimated_savings_kwh": round(hvac_kwh, 2),
            "estimated_savings_inr": round(hvac_cost, 2),
            "carbon_reduction_kg": round(hvac_carbon, 2),
            "priority": "High"
        },
        {
            "category": "Lighting Optimization",
            "recommendation": "Enable daylight harvesting controls and schedule automated LED dimming after 19:00.",
            "energy_saving_pct": lighting_saving_pct,
            "estimated_savings_kwh": round(lighting_kwh, 2),
            "estimated_savings_inr": round(lighting_cost, 2),
            "carbon_reduction_kg": round(lighting_carbon, 2),
            "priority": "Medium"
        },
        {
            "category": "Equipment Scheduling",
            "recommendation": "Stagger heavy laboratory equipment and autoclave cycles during non-peak utility hours.",
            "energy_saving_pct": equip_saving_pct,
            "estimated_savings_kwh": round(equip_kwh, 2),
            "estimated_savings_inr": round(equip_cost, 2),
            "carbon_reduction_kg": round(equip_carbon, 2),
            "priority": "High"
        },
        {
            "category": "Peak Load Shifting",
            "recommendation": f"Shift {peak_shift_kwh:.1f} kWh of non-critical loads away from 14:00 - 18:00 tariff peak.",
            "energy_saving_pct": 12.0,
            "estimated_savings_kwh": round(peak_shift_kwh, 2),
            "estimated_savings_inr": round(peak_shift_kwh * PRICE_PER_KWH, 2),
            "carbon_reduction_kg": round(peak_shift_kwh * CARBON_PER_KWH, 2),
            "priority": "High"
        },
        {
            "category": "Solar Utilization",
            "recommendation": f"Direct {solar_utilization_kw:.0f} kW rooftop PV output to high-demand computer lab clusters.",
            "energy_saving_pct": 18.0,
            "estimated_savings_kwh": round(solar_utilization_kw * 4, 2),
            "estimated_savings_inr": round(solar_utilization_kw * 4 * PRICE_PER_KWH, 2),
            "carbon_reduction_kg": round(solar_utilization_kw * 4 * CARBON_PER_KWH, 2),
            "priority": "Medium"
        },
        {
            "category": "Battery Energy Storage",
            "recommendation": f"Pre-charge campus BESS ({battery_utilization_kwh:.0f} kWh) during night tariffs for peak discharge.",
            "energy_saving_pct": 9.5,
            "estimated_savings_kwh": round(battery_utilization_kwh, 2),
            "estimated_savings_inr": round(battery_utilization_kwh * PRICE_PER_KWH, 2),
            "carbon_reduction_kg": round(battery_utilization_kwh * CARBON_PER_KWH, 2),
            "priority": "Low"
        }
    ]

    # Save to reports/optimization_report.csv
    try:
        df_rec = pd.DataFrame(recommendations_list)
        df_rec.to_csv(REPORTS_DIR / "optimization_report.csv", index=False)
    except Exception as e:
        logger.error(f"Failed to export optimization report CSV: {e}")

    return {
        "building": building,
        "current_energy_kwh": current_energy,
        "total_potential_savings_kwh": round(total_kwh_saved, 2),
        "total_potential_savings_inr": round(total_cost_saved, 2),
        "total_carbon_reduction_kg": round(total_carbon_reduced, 2),
        "expected_annual_savings_inr": round(expected_annual_savings, 2),
        "recommendations": recommendations_list
    }