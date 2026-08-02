import pandas as pd


def load_dataset():

    return pd.read_csv(
        "data/processed/campus_energy_features.csv"
    )


def total_energy(df):

    return round(
        df["Energy_kWh"].sum(),
        2
    )


def average_energy(df):

    return round(
        df["Energy_kWh"].mean(),
        2
    )


def total_cost(df):

    return round(
        df["Cost"].sum(),
        2
    )


def total_carbon(df):

    return round(
        df["Carbon_Emission"].sum(),
        2
    )


def building_consumption(df):

    return df.groupby(
        "Building"
    )["Energy_kWh"].sum().reset_index()


def hourly_consumption(df):

    return df.groupby(
        "Hour"
    )["Energy_kWh"].mean().reset_index()