import pandas as pd

report = pd.read_csv(
    "reports/optimization_report.csv"
)

print("\n")
print("=" * 70)
print(" CAMPUS ENERGY OPTIMIZATION REPORT ")
print("=" * 70)

total_energy = report["Energy_kWh"].sum()
total_cost = report["Electricity_Cost"].sum()
total_carbon = report["Carbon_Emission"].sum()

print(f"Total Energy Consumed : {total_energy:,.2f} kWh")
print(f"Total Electricity Cost: ₹{total_cost:,.2f}")
print(f"Total Carbon Emission : {total_carbon:,.2f} kg CO₂")

print("\nTop 5 High Consumption Buildings\n")

print(
    report[
        [
            "Building",
            "Energy_kWh",
            "Recommendation"
        ]
    ].head()
)