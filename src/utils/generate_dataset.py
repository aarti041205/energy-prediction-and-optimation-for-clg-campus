import pandas as pd
import numpy as np

np.random.seed(42)

buildings = [
    ("Hostel_A", "Hostel"),
    ("Hostel_B", "Hostel"),
    ("Block_A", "Classroom"),
    ("Block_B", "Classroom"),
    ("AI_Lab", "Lab"),
    ("Robotics_Lab", "Lab"),
    ("Central_Library", "Library"),
    ("Sports_Complex", "Sports"),
    ("Admin_Block", "Administration"),
    ("Cafeteria", "Cafeteria")
]

timestamps = pd.date_range(
    start="2025-01-01",
    end="2025-12-31 23:00",
    freq="h"
)

rows = []

for ts in timestamps:

    hour = ts.hour
    month = ts.month
    weekend = 1 if ts.weekday() >= 5 else 0

    holiday = np.random.choice([0, 1], p=[0.96, 0.04])
    exam = np.random.choice([0, 1], p=[0.92, 0.08])

    temperature = np.random.normal(28, 4)
    humidity = np.random.normal(65, 10)

    for building, btype in buildings:

        occupancy = np.random.randint(20, 400)

        equipment = np.random.randint(20, 100) if btype == "Lab" else np.random.randint(5, 40)

        solar = max(0, np.random.normal(40, 15)) if 7 <= hour <= 17 else 0

        base = {
            "Hostel": 450,
            "Classroom": 300,
            "Lab": 500,
            "Library": 250,
            "Sports": 220,
            "Administration": 180,
            "Cafeteria": 260
        }

        energy = (
            base[btype]
            + occupancy * 0.5
            + equipment * 1.2
            + temperature * 2
            - solar * 0.6
            + np.random.normal(0, 20)
        )

        cost = energy * 8

        carbon = energy * 0.82

        rows.append([
            ts,
            building,
            btype,
            round(energy, 2),
            round(temperature, 2),
            round(humidity, 2),
            occupancy,
            holiday,
            exam,
            weekend,
            round(solar, 2),
            equipment,
            round(carbon, 2),
            round(cost, 2)
        ])

columns = [
    "Timestamp",
    "Building",
    "Building_Type",
    "Energy_kWh",
    "Temperature",
    "Humidity",
    "Occupancy",
    "Holiday",
    "Exam_Day",
    "Weekend",
    "Solar_Output",
    "Equipment_Load",
    "Carbon_Emission",
    "Cost"
]

df = pd.DataFrame(rows, columns=columns)

df.to_csv("data/raw/campus_energy.csv", index=False)

print(df.head())

print(df.shape)