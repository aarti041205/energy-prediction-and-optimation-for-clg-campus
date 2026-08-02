import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.models.random_forest import get_random_forest
from src.models.xgboost_model import get_xgboost
from src.models.evaluate import evaluate_model

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

df = pd.read_csv("data/processed/campus_energy_features.csv")

# Features and Target
X = df.drop(columns=["Energy_kWh", "Timestamp"])
y = df["Energy_kWh"]

# ---------------------------------------------------
# Preprocessing
# ---------------------------------------------------

categorical = [
    "Building",
    "Building_Type"
]

numerical = [
    col for col in X.columns
    if col not in categorical
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

# ---------------------------------------------------
# Time-Series Train/Test Split
# ---------------------------------------------------

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# ---------------------------------------------------
# Models
# ---------------------------------------------------

models = {
    "Random Forest": get_random_forest(),
    "XGBoost": get_xgboost()
}

results = []

best_pipeline = None
best_model = None
best_rmse = float("inf")

os.makedirs("saved_models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ---------------------------------------------------
# Train Models
# ---------------------------------------------------

for model_name, model in models.items():

    print(f"\n==============================")
    print(f"Training {model_name}")
    print(f"==============================")

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X_train, y_train)

    metrics = evaluate_model(
        pipeline,
        X_test,
        y_test
    )

    metrics["Model"] = model_name

    results.append(metrics)

    print(metrics)

    # Save every model
    filename = model_name.lower().replace(" ", "_") + ".pkl"

    joblib.dump(
        pipeline,
        f"saved_models/{filename}"
    )

    print(f"{model_name} saved.")

    # Keep track of best model
    if metrics["RMSE"] < best_rmse:
        best_rmse = metrics["RMSE"]
        best_model = model_name
        best_pipeline = pipeline

# ---------------------------------------------------
# Save Comparison Report
# ---------------------------------------------------

comparison = pd.DataFrame(results)

comparison = comparison[
    [
        "Model",
        "MAE",
        "RMSE",
        "R2",
        "MAPE"
    ]
]

comparison.to_csv(
    "reports/model_comparison.csv",
    index=False
)

print("\n==============================")
print("Model Comparison")
print("==============================")

print(comparison)

# ---------------------------------------------------
# Save Best Model
# ---------------------------------------------------

joblib.dump(
    best_pipeline,
    "saved_models/best_model.pkl"
)

print(f"\nBest Model : {best_model}")
print(f"Best RMSE  : {best_rmse:.4f}")

print("\nTraining Completed Successfully!")