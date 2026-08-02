import pandas as pd
from src.database.db_connection import engine

# Load processed dataset
df = pd.read_csv("data/processed/campus_energy_processed.csv")

# Load into PostgreSQL
df.to_sql(
    name="energy_usage",
    con=engine,
    if_exists="replace",
    index=False
)

print("✅ Dataset loaded successfully into PostgreSQL!")
print(f"Rows inserted: {len(df)}")