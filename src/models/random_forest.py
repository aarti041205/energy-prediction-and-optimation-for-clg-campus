from sklearn.ensemble import RandomForestRegressor

def get_random_forest():
    return RandomForestRegressor(
        n_estimators=200,
        max_depth=20,
        random_state=42,
        n_jobs=-1
    )