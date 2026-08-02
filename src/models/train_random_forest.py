import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("data/processed/campus_energy_processed.csv")

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# -----------------------------
# Feature Engineering
# -----------------------------
df["Year"] = df["Timestamp"].dt.year
df["Month"] = df["Timestamp"].dt.month
df["Day"] = df["Timestamp"].dt.day
df["Hour"] = df["Timestamp"].dt.hour
df["DayOfWeek"] = df["Timestamp"].dt.dayofweek

# -----------------------------
# Features & Target
# -----------------------------
X = df.drop(columns=["Energy_kWh", "Timestamp"])
y = df["Energy_kWh"]

categorical = [
    "Building",
    "Building_Type"
]

numerical = [
    c for c in X.columns
    if c not in categorical
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical
        ),
        (
            "num",
            "passthrough",
            numerical
        )
    ]
)

# -----------------------------
# Split Data
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Build Pipeline
# -----------------------------
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ))
])

# -----------------------------
# Train
# -----------------------------
print("Training model...")

model.fit(X_train, y_train)

print("Training completed!")

# -----------------------------
# Predict
# -----------------------------
predictions = model.predict(X_test)

# -----------------------------
# Evaluation
# -----------------------------
import numpy as np

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = np.sqrt(mse)

import numpy as np

mae = mean_absolute_error(y_test, predictions)

mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)

r2 = r2_score(y_test, predictions)

print("\nModel Performance")
print("---------------------")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")

# -----------------------------
# Save Model
# -----------------------------
os.makedirs("saved_models", exist_ok=True)

joblib.dump(
    model,
    "saved_models/random_forest_model.pkl"
)

print("\nModel saved successfully!")