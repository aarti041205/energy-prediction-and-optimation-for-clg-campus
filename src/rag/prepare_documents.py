import os
import pandas as pd

os.makedirs("knowledge_base", exist_ok=True)

reports = {
    "building_summary.csv": "building_summary.txt",
    "optimization_report.csv": "optimization_report.txt",
    "anomaly_report.csv": "anomaly_report.txt"
}

for csv_file, txt_file in reports.items():

    path = f"reports/{csv_file}"

    if not os.path.exists(path):
        print(f"Skipping {csv_file}")
        continue

    df = pd.read_csv(path)

    with open(f"knowledge_base/{txt_file}", "w", encoding="utf-8") as f:

        for _, row in df.iterrows():
            f.write(row.to_string())
            f.write("\n")
            f.write("-"*60)
            f.write("\n")

print("Knowledge base created successfully.")