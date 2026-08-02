import pandas as pd

df = pd.read_csv(
    "reports/anomaly_report.csv"
)

anomalies = df[
    df["Anomaly"] == -1
]

print(anomalies.head())

anomalies.to_csv(
    "reports/only_anomalies.csv",
    index=False
)

print(f"Total anomalies: {len(anomalies)}")