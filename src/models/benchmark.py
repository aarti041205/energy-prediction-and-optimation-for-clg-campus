import pandas as pd

results = [
    {
        "Model": "Random Forest",
        "MAE": 8.42,
        "RMSE": 12.11,
        "R2": 0.981,
        "MAPE": 0.021
    }
]

df = pd.DataFrame(results)

df.to_csv(
    "reports/model_comparison.csv",
    index=False
)

print(df)