import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path("saved_models/random_forest.pkl")

model = joblib.load(MODEL_PATH)

def predict_energy(features: dict):

    df = pd.DataFrame([features])

    prediction = model.predict(df)[0]

    return round(float(prediction), 2)