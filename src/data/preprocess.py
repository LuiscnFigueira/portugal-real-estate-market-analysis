from __future__ import annotations

import pandas as pd

from src.config import REFERENCE_YEAR
from src.features.build_features import add_initial_features


COLUMN_NAMES = [
    "price",
    "district",
    "city",
    "town",
    "type",
    "energy_certificate",
    "gross_area",
    "total_area",
    "parking",
    "has_parking",
    "floor",
    "construction_year",
    "energy_efficiency_level",
    "publish_date",
    "garage",
    "elevator",
    "electric_cars_charging",
    "total_rooms",
    "number_of_bedrooms",
    "number_of_wc",
    "conservation_status",
    "living_area",
    "lot_size",
    "built_area",
    "number_of_bathrooms",
]

BOOLEAN_COLUMNS = [
    "has_parking",
    "garage",
    "elevator",
    "electric_cars_charging",
]

CATEGORICAL_COLUMNS = [
    "district",
    "city",
    "town",
    "type",
    "energy_certificate",
    "floor",
    "energy_efficiency_level",
    "conservation_status",
]

INTEGER_COLUMNS = [
    "parking",
    "construction_year",
    "total_rooms",
    "number_of_bedrooms",
    "number_of_wc",
    "number_of_bathrooms",
]


def load_raw_data(path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if len(df.columns) != len(COLUMN_NAMES):
        raise ValueError(
            f"Número inesperado de colunas: {len(df.columns)}. "
            f"Esperado: {len(COLUMN_NAMES)}."
        )
    df.columns = COLUMN_NAMES
    return df


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")

    for col in BOOLEAN_COLUMNS:
        boolean_map = {
            "true": True,
            "false": False,
            "yes": True,
            "no": False,
            "sim": True,
            "não": False,
            "nao": False,
        }
        normalized = df[col].astype("string").str.lower().str.strip()
        df[col] = normalized.map(boolean_map).astype("boolean")

    for col in CATEGORICAL_COLUMNS:
        df[col] = df[col].astype("category")

    for col in INTEGER_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    return df


def mark_invalid_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.loc[df["price"] <= 0, "price"] = pd.NA
    df.loc[df["total_area"] <= 0, "total_area"] = pd.NA

    area_columns = ["gross_area", "living_area", "lot_size", "built_area"]
    for col in area_columns:
        df.loc[df[col] <= 0, col] = pd.NA

    count_columns = ["number_of_wc", "number_of_bathrooms"]
    for col in count_columns:
        df.loc[df[col] < 0, col] = pd.NA

    return df


def clean_initial_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna(subset=["price"])
    return df


def build_initial_dataset(df: pd.DataFrame, reference_year: int = REFERENCE_YEAR) -> pd.DataFrame:
    df = rename_columns(df)
    df = convert_types(df)
    df = mark_invalid_values(df)
    df = add_initial_features(df, reference_year=reference_year)
    df = clean_initial_data(df)
    return df
