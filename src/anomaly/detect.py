import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# -------------------------
# Load Data
# -------------------------

df = pd.read_csv(
    "data/processed/campus_energy_features.csv"
)

# -------------------------
# Features
# -------------------------

X = df.drop(
    columns=["Energy_kWh", "Timestamp"]
)

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

pipeline = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "detector",
        IsolationForest(
            contamination=0.02,
            random_state=42
        )
    )
])

print("Training Anomaly Detector...")

pipeline.fit(X)

predictions = pipeline.predict(X)

df["Anomaly"] = predictions

os.makedirs("saved_models", exist_ok=True)

joblib.dump(
    pipeline,
    "saved_models/anomaly_detector.pkl"
)

print("Anomaly model saved.")

print(df["Anomaly"].value_counts())

df.to_csv(
    "reports/anomaly_report.csv",
    index=False
)

print("Report Generated.")