import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# -----------------------
# Load Dataset
# -----------------------

df = pd.read_csv(
    "data/processed/campus_energy_features.csv"
)

# -----------------------
# Features used in API
# -----------------------

features = [
    "Building",
    "Building_Type",
    "Temperature",
    "Humidity",
    "Hour",
    "Day",
    "Month",
    "Weekend",
    "Holiday",
    "Equipment_Load"
]

target = "Energy_kWh"

X = df[features]
y = df[target]

# -----------------------
# Split Data
# -----------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------
# Preprocessing
# -----------------------

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

# -----------------------
# Model
# -----------------------

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    (
        "model",
        RandomForestRegressor(
            n_estimators=300,
            random_state=42
        )
    )
])

print("Training deployment model...")

pipeline.fit(
    X_train,
    y_train
)

predictions = pipeline.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)

print()

print("Deployment Model Performance")

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")

os.makedirs(
    "saved_models",
    exist_ok=True
)

joblib.dump(
    pipeline,
    "saved_models/deployment_model.pkl"
)

print()

print("Deployment model saved successfully.")