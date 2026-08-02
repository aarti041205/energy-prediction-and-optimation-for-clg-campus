import joblib

def save_model(model, path):
    joblib.dump(model, path)
    print(f"Model saved at {path}")

def load_model(path):
    return joblib.load(path)