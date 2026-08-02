# from extract import extract_data
# from transform import transform_data
# from load import save_processed_data
from .extract import extract_data
from .transform import transform_data
from .load import save_processed_data

def run_pipeline():

    raw_file = "data/raw/campus_energy.csv"

    processed_file = "data/processed/campus_energy_processed.csv"

    df = extract_data(raw_file)

    df = transform_data(df)

    save_processed_data(df, processed_file)


if __name__ == "__main__":
    run_pipeline()