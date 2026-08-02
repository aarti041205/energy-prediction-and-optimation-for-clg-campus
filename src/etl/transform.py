import pandas as pd

def transform_data(df):

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert Timestamp
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Handle missing values
    df = df.ffill().bfill()

    # Feature Engineering
    df["Year"] = df["Timestamp"].dt.year
    df["Month"] = df["Timestamp"].dt.month
    df["Day"] = df["Timestamp"].dt.day
    df["Hour"] = df["Timestamp"].dt.hour
    df["DayOfWeek"] = df["Timestamp"].dt.dayofweek

    return df