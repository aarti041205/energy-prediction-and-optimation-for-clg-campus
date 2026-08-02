import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(
    "reports/anomaly_report.csv"
)

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

normal = df[df["Anomaly"] == 1]
anomaly = df[df["Anomaly"] == -1]

plt.figure(figsize=(15,6))

plt.scatter(
    normal["Timestamp"],
    normal["Energy_kWh"],
    s=5,
    label="Normal"
)

plt.scatter(
    anomaly["Timestamp"],
    anomaly["Energy_kWh"],
    s=20,
    label="Anomaly"
)

plt.legend()

plt.title("Energy Consumption Anomalies")

plt.xlabel("Timestamp")

plt.ylabel("Energy (kWh)")

plt.tight_layout()

plt.show()