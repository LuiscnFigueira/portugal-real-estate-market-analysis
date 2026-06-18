from __future__ import annotations

import numpy as np
import pandas as pd


def add_initial_features(df: pd.DataFrame, reference_year: int) -> pd.DataFrame:
    df = df.copy()

    df["price_m2"] = df["price"] / df["total_area"]
    df["price_m2"] = df["price_m2"].replace([np.inf, -np.inf], np.nan)
    df.loc[df["price_m2"] <= 0, "price_m2"] = np.nan

    df["property_age"] = reference_year - df["construction_year"]
    df.loc[df["property_age"] < 0, "property_age"] = pd.NA

    df["publish_year"] = df["publish_date"].dt.year
    df["publish_month"] = df["publish_date"].dt.month

    return df


def modeling_excluded_features() -> list[str]:
    return [
        "price",
        "log_price",
        "price_m2",
        "price_iqr_outlier",
        "price_m2_iqr_outlier",
    ]


def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    result = numerator / denominator.replace(0, np.nan)
    return result.replace([np.inf, -np.inf], np.nan)


def _log1p_positive(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    return np.log1p(numeric.where(numeric >= 0))


def _boolean_signal(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False).astype(bool)

    normalized = series.astype("string").str.lower().str.strip()
    mapped = normalized.map(
        {
            "true": True,
            "false": False,
            "yes": True,
            "no": False,
            "sim": True,
            "não": False,
            "nao": False,
            "1": True,
            "0": False,
        }
    )
    return mapped.fillna(False).astype(bool)


def add_modeling_features(df: pd.DataFrame) -> pd.DataFrame:
    """Cria features candidatas sem usar diretamente a variável alvo."""
    features = df.copy()

    if "price" in features.columns:
        features["log_price"] = _log1p_positive(features["price"])

    for col in ["total_area", "living_area", "gross_area", "lot_size", "built_area"]:
        if col in features.columns:
            features[f"log_{col}"] = _log1p_positive(features[col])

    if {"living_area", "total_area"}.issubset(features.columns):
        features["living_total_area_ratio"] = _safe_divide(
            features["living_area"], features["total_area"]
        )

    if {"gross_area", "total_area"}.issubset(features.columns):
        features["gross_total_area_ratio"] = _safe_divide(
            features["gross_area"], features["total_area"]
        )

    if {"built_area", "total_area"}.issubset(features.columns):
        features["built_total_area_ratio"] = _safe_divide(
            features["built_area"], features["total_area"]
        )

    if {"number_of_bedrooms", "total_rooms"}.issubset(features.columns):
        features["bedrooms_per_room"] = _safe_divide(
            features["number_of_bedrooms"], features["total_rooms"]
        )

    if {"number_of_bathrooms", "number_of_bedrooms"}.issubset(features.columns):
        features["bathrooms_per_bedroom"] = _safe_divide(
            features["number_of_bathrooms"], features["number_of_bedrooms"]
        )

    if {"total_rooms", "number_of_bathrooms"}.issubset(features.columns):
        features["rooms_per_bathroom"] = _safe_divide(
            features["total_rooms"], features["number_of_bathrooms"]
        )

    amenity_cols = [
        col
        for col in ["has_parking", "garage", "elevator", "electric_cars_charging"]
        if col in features.columns
    ]
    if amenity_cols:
        amenity_frame = pd.DataFrame(
            {col: _boolean_signal(features[col]).astype("Int64") for col in amenity_cols},
            index=features.index,
        )
        features["amenity_count"] = amenity_frame.sum(axis=1, min_count=1)

    if {"parking", "has_parking", "garage"}.intersection(features.columns):
        parking_signal = pd.Series(False, index=features.index)
        if "parking" in features.columns:
            parking_signal = parking_signal | (pd.to_numeric(features["parking"], errors="coerce") > 0)
        if "has_parking" in features.columns:
            parking_signal = parking_signal | _boolean_signal(features["has_parking"])
        if "garage" in features.columns:
            parking_signal = parking_signal | _boolean_signal(features["garage"])
        features["has_parking_or_garage"] = parking_signal

    missing_cols = [
        col
        for col in features.columns
        if col.endswith("_missing")
        and col
        in {
            "gross_area_missing",
            "living_area_missing",
            "lot_size_missing",
            "built_area_missing",
            "construction_year_missing",
            "total_rooms_missing",
            "number_of_bedrooms_missing",
            "number_of_wc_missing",
            "number_of_bathrooms_missing",
        }
    ]
    if missing_cols:
        features["missing_core_feature_count"] = features[missing_cols].sum(axis=1)

    if "construction_year" in features.columns:
        construction_year = pd.to_numeric(features["construction_year"], errors="coerce")
        features["construction_decade"] = (construction_year // 10 * 10).astype("Int64")

    if "property_age" in features.columns:
        features["property_age_group"] = pd.cut(
            pd.to_numeric(features["property_age"], errors="coerce"),
            bins=[-1, 5, 15, 30, 60, np.inf],
            labels=["0-5", "6-15", "16-30", "31-60", "60+"],
        ).astype("string")

    if "publish_month" in features.columns:
        publish_month = pd.to_numeric(features["publish_month"], errors="coerce")
        features["publish_quarter"] = (((publish_month - 1) // 3) + 1).astype("Int64")
        features["publish_month_sin"] = np.sin(2 * np.pi * publish_month / 12)
        features["publish_month_cos"] = np.cos(2 * np.pi * publish_month / 12)

    if {"district", "type"}.issubset(features.columns):
        features["district_type"] = (
            features["district"].astype("string").fillna("unknown")
            + "__"
            + features["type"].astype("string").fillna("unknown")
        )

    if {"city", "type"}.issubset(features.columns):
        features["city_type"] = (
            features["city"].astype("string").fillna("unknown")
            + "__"
            + features["type"].astype("string").fillna("unknown")
        )

    return features


def modeling_feature_columns(df: pd.DataFrame) -> list[str]:
    """Lista colunas candidatas para modelação, excluindo alvo e leakage óbvio."""
    excluded = set(modeling_excluded_features())
    excluded.update(
        col
        for col in df.columns
        if col.endswith("_iqr_outlier")
    )
    return [col for col in df.columns if col not in excluded]
