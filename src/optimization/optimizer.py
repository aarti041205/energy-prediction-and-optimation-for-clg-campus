import os
import pandas as pd

# ----------------------------------
# Configuration
# ----------------------------------

PRICE_PER_KWH = 8.5          # ₹ per unit
CARBON_PER_KWH = 0.82        # kg CO₂

# ----------------------------------
# Load Data
# ----------------------------------

df = pd.read_csv(
    "data/processed/campus_energy_features.csv"
)

# ----------------------------------
# Calculate Cost
# ----------------------------------

df["Electricity_Cost"] = (
    df["Energy_kWh"] * PRICE_PER_KWH
)

# ----------------------------------
# Carbon Footprint
# ----------------------------------

df["Carbon_Emission"] = (
    df["Energy_kWh"] * CARBON_PER_KWH
)

# ----------------------------------
# Building Summary
# ----------------------------------

summary = (
    df.groupby("Building")
    .agg({
        "Energy_kWh":"sum",
        "Electricity_Cost":"sum",
        "Carbon_Emission":"sum"
    })
    .reset_index()
)

summary = summary.sort_values(
    "Energy_kWh",
    ascending=False
)

os.makedirs("reports", exist_ok=True)

summary.to_csv(
    "reports/building_summary.csv",
    index=False
)

print(summary)