import pandas as pd

def engineer_features(df):

    # Convert Timestamp
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Time Features
    df["Year"] = df["Timestamp"].dt.year
    df["Month"] = df["Timestamp"].dt.month
    df["Day"] = df["Timestamp"].dt.day
    df["Hour"] = df["Timestamp"].dt.hour
    df["DayOfWeek"] = df["Timestamp"].dt.dayofweek

    # Weekend Flag
    df["IsWeekend"] = (df["DayOfWeek"] >= 5).astype(int)

    return df