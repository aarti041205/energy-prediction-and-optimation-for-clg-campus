import pandas as pd
from sqlalchemy import text
from src.database.db_connection import engine

query = text("""
SELECT
    "Building",
    AVG("Energy_kWh") AS avg_energy
FROM energy_usage
GROUP BY "Building"
ORDER BY avg_energy DESC;
""")

df = pd.read_sql(query, engine)


print(df)

df.to_csv(
    "reports/building_energy_summary.csv",
    index=False
)

print("Report saved successfully!")