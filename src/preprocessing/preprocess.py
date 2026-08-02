import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from .feature_engineering import engineer_features


def preprocess_data():

    df = pd.read_csv(
        "data/processed/campus_energy_processed.csv"
    )

    df = engineer_features(df)

    X = df.drop(
        columns=[
            "Energy_kWh",
            "Timestamp"
        ]
    )

    y = df["Energy_kWh"]

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

    pipeline = Pipeline([
        ("preprocessor", preprocessor)
    ])

    X_processed = pipeline.fit_transform(X)

    joblib.dump(
        pipeline,
        "src/models/preprocessing_pipeline.pkl"
    )

    return X_processed, y