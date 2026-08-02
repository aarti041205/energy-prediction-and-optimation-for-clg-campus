import pandas as pd

df = pd.read_csv("data/processed/campus_energy_processed.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

df = df.sort_values(
    ["Building", "Timestamp"]
)

df["Lag_1"] = (
    df.groupby("Building")["Energy_kWh"]
      .shift(1)
)

df["Lag_24"] = (
    df.groupby("Building")["Energy_kWh"]
      .shift(24)
)

df["Lag_168"] = (
    df.groupby("Building")["Energy_kWh"]
      .shift(168)
)

df["RollingMean_3"] = (
    df.groupby("Building")["Energy_kWh"]
      .transform(lambda x: x.rolling(3).mean())
)

df["RollingMean_24"] = (
    df.groupby("Building")["Energy_kWh"]
      .transform(lambda x: x.rolling(24).mean())
)

df["RollingStd_24"] = (
    df.groupby("Building")["Energy_kWh"]
      .transform(lambda x: x.rolling(24).std())
)

import numpy as np

df["Hour_Sin"] = np.sin(
    2 * np.pi * df["Hour"] / 24
)

df["Hour_Cos"] = np.cos(
    2 * np.pi * df["Hour"] / 24
)

df["Day_Sin"] = np.sin(
    2 * np.pi * df["DayOfWeek"] / 7
)

df["Day_Cos"] = np.cos(
    2 * np.pi * df["DayOfWeek"] / 7
)


df = df.dropna()

df.to_csv(
    "data/processed/campus_energy_features.csv",
    index=False
)

print(df.head())
print(df.shape)
