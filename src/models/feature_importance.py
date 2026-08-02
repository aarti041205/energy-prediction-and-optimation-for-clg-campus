import joblib
import pandas as pd
import matplotlib.pyplot as plt

model = joblib.load("saved_models/xgboost.pkl")

feature_names = model.named_steps["preprocessor"].get_feature_names_out()

importance = model.named_steps["model"].feature_importances_

importance_df = (
    pd.DataFrame({
        "Feature": feature_names,
        "Importance": importance
    })
    .sort_values("Importance", ascending=False)
)

print(importance_df.head(20))

plt.figure(figsize=(10,6))

plt.barh(
    importance_df["Feature"].head(15),
    importance_df["Importance"].head(15)
)

plt.gca().invert_yaxis()

plt.title("Top 15 Important Features")

plt.tight_layout()

plt.show()