from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import REFERENCE_YEAR


AREA_COLUMNS = ["gross_area", "total_area", "living_area", "lot_size", "built_area"]

COUNT_COLUMNS = [
    "parking",
    "total_rooms",
    "number_of_bedrooms",
    "number_of_wc",
    "number_of_bathrooms",
]

OUTLIER_COLUMNS = [
    "price",
    "gross_area",
    "total_area",
    "living_area",
    "lot_size",
    "built_area",
    "total_rooms",
    "number_of_bathrooms",
    "price_m2",
]

MISSING_INDICATOR_COLUMNS = [
    "gross_area",
    "living_area",
    "lot_size",
    "built_area",
    "construction_year",
    "total_rooms",
    "number_of_bedrooms",
    "number_of_wc",
    "number_of_bathrooms",
    "energy_certificate",
    "conservation_status",
]


def normalize_text_values(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza espaços e strings vazias sem alterar categorias válidas."""
    df = df.copy()
    text_columns = df.select_dtypes(include=["object", "category", "string"]).columns

    for col in text_columns:
        normalized = df[col].astype("string").str.strip()
        normalized = normalized.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
        df[col] = normalized

    return df


def enforce_domain_rules(
    df: pd.DataFrame,
    reference_year: int = REFERENCE_YEAR,
) -> pd.DataFrame:
    """Aplica regras objetivas de domínio sem remover outliers contextuais."""
    df = df.copy()

    if "price" in df.columns:
        df.loc[df["price"] <= 0, "price"] = np.nan

    for col in AREA_COLUMNS:
        if col in df.columns:
            df.loc[df[col] <= 0, col] = np.nan

    for col in COUNT_COLUMNS:
        if col in df.columns:
            df.loc[df[col] < 0, col] = np.nan

    if "construction_year" in df.columns:
        invalid_year = (df["construction_year"] < 1900) | (
            df["construction_year"] > reference_year
        )
        df.loc[invalid_year, "construction_year"] = np.nan

    if {"construction_year", "property_age"}.issubset(df.columns):
        df["property_age"] = reference_year - df["construction_year"]
        df.loc[df["property_age"] < 0, "property_age"] = np.nan

    if {"price", "total_area", "price_m2"}.issubset(df.columns):
        df["price_m2"] = df["price"] / df["total_area"]
        df["price_m2"] = df["price_m2"].replace([np.inf, -np.inf], np.nan)
        df.loc[df["price_m2"] <= 0, "price_m2"] = np.nan

    return df


def add_missing_indicators(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """Cria indicadores de ausência para variáveis relevantes."""
    df = df.copy()
    columns = columns or MISSING_INDICATOR_COLUMNS

    for col in columns:
        if col in df.columns:
            df[f"{col}_missing"] = df[col].isna()

    return df


def calculate_iqr_outlier_summary(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """Calcula limites IQR para diagnóstico, sem remover linhas."""
    columns = columns or OUTLIER_COLUMNS
    rows = []

    for col in columns:
        if col not in df.columns:
            continue

        series = pd.to_numeric(df[col], errors="coerce").dropna()
        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        count = int(((series < lower) | (series > upper)).sum())

        rows.append(
            {
                "column": col,
                "q1": q1,
                "q3": q3,
                "iqr": iqr,
                "lower_bound": lower,
                "upper_bound": upper,
                "outlier_count": count,
                "outlier_share": count / len(series),
            }
        )

    return pd.DataFrame(rows)


def add_iqr_outlier_flags(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> pd.DataFrame:
    """Sinaliza outliers por IQR, mantendo as observações no dataset."""
    df = df.copy()
    summary = calculate_iqr_outlier_summary(df, columns=columns)

    for row in summary.itertuples(index=False):
        col = row.column
        flag_col = f"{col}_iqr_outlier"
        df[flag_col] = (df[col] < row.lower_bound) | (df[col] > row.upper_bound)
        df[flag_col] = df[flag_col].fillna(False)

    return df


def prepare_dataset(
    df: pd.DataFrame,
    reference_year: int = REFERENCE_YEAR,
) -> pd.DataFrame:
    """Prepara o dataset para análise e fases futuras de modelação."""
    prepared = df.copy()
    prepared = normalize_text_values(prepared)
    prepared = enforce_domain_rules(prepared, reference_year=reference_year)
    prepared = prepared.drop_duplicates()
    prepared = prepared.dropna(subset=["price"])
    prepared = add_missing_indicators(prepared)
    prepared = add_iqr_outlier_flags(prepared)
    prepared = prepared.reset_index(drop=True)
    return prepared
