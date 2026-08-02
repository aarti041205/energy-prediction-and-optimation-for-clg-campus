import pandas as pd

df = pd.read_csv(
    "reports/only_anomalies.csv"
)

for _, row in df.head(10).iterrows():

    print("=" * 60)

    print(f"Building : {row['Building']}")

    print(f"Time     : {row['Timestamp']}")

    print(f"Energy   : {row['Energy_kWh']:.2f} kWh")

    print("⚠ ALERT : Abnormal Energy Consumption Detected")

    print("=" * 60)