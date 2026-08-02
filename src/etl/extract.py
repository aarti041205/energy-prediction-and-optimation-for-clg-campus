import pandas as pd

def extract_data(file_path):
    """
    Read raw CSV file.
    """
    df = pd.read_csv(file_path)

    print(f"Data loaded successfully!")
    print(f"Rows: {len(df)}")

    return df