from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression


def target_distribution_summary(df: pd.DataFrame, target: str = "price") -> pd.DataFrame:
    series = pd.to_numeric(df[target], errors="coerce").dropna()
    percentiles = [0.01, 0.05, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]

    summary = {
        "count": series.count(),
        "mean": series.mean(),
        "std": series.std(),
        "min": series.min(),
        "skew": series.skew(),
        "kurtosis": series.kurtosis(),
        "max": series.max(),
    }
    summary.update({f"p{int(p * 100)}": series.quantile(p) for p in percentiles})
    return pd.DataFrame([summary]).T.rename(columns={0: target})


def numeric_association_summary(
    df: pd.DataFrame,
    target: str = "log_price",
    columns: list[str] | None = None,
    min_pairs: int = 100,
) -> pd.DataFrame:
    result_columns = [
        "feature",
        "n_pairs",
        "pearson_r",
        "pearson_p",
        "spearman_r",
        "spearman_p",
        "abs_spearman_r",
    ]
    numeric_cols = columns or df.select_dtypes(include="number").columns.tolist()
    rows = []

    for col in numeric_cols:
        if col == target:
            continue

        pairs = df[[target, col]].apply(pd.to_numeric, errors="coerce").dropna()
        if len(pairs) < min_pairs:
            continue

        pearson_r, pearson_p = stats.pearsonr(pairs[col], pairs[target])
        spearman_r, spearman_p = stats.spearmanr(pairs[col], pairs[target])
        rows.append(
            {
                "feature": col,
                "n_pairs": len(pairs),
                "pearson_r": pearson_r,
                "pearson_p": pearson_p,
                "spearman_r": spearman_r,
                "spearman_p": spearman_p,
                "abs_spearman_r": abs(spearman_r),
            }
        )

    if not rows:
        return pd.DataFrame(columns=result_columns)

    return (
        pd.DataFrame(rows, columns=result_columns)
        .sort_values("abs_spearman_r", ascending=False)
        .reset_index(drop=True)
    )


def group_distribution_summary(
    df: pd.DataFrame,
    category: str,
    target: str = "log_price",
    min_group_size: int = 100,
) -> pd.DataFrame:
    data = df[[category, target]].dropna()
    counts = data[category].value_counts()
    valid_categories = counts[counts >= min_group_size].index
    data = data[data[category].isin(valid_categories)]

    grouped = data.groupby(category, observed=True)[target]
    return (
        grouped.agg(
            n="count",
            mean="mean",
            median="median",
            std="std",
            q1=lambda s: s.quantile(0.25),
            q3=lambda s: s.quantile(0.75),
        )
        .sort_values("median", ascending=False)
        .reset_index()
    )


def kruskal_group_test(
    df: pd.DataFrame,
    category: str,
    target: str = "log_price",
    min_group_size: int = 100,
) -> dict[str, float | int | str]:
    data = df[[category, target]].dropna()
    counts = data[category].value_counts()
    valid_categories = counts[counts >= min_group_size].index
    data = data[data[category].isin(valid_categories)]

    groups = [group[target].to_numpy() for _, group in data.groupby(category, observed=True)]
    if len(groups) < 2:
        return {
            "category": category,
            "groups": len(groups),
            "n": len(data),
            "h_statistic": np.nan,
            "p_value": np.nan,
            "epsilon_squared": np.nan,
        }

    h_statistic, p_value = stats.kruskal(*groups)
    n = len(data)
    k = len(groups)
    epsilon_squared = (h_statistic - k + 1) / (n - k) if n > k else np.nan

    return {
        "category": category,
        "groups": k,
        "n": n,
        "h_statistic": h_statistic,
        "p_value": p_value,
        "epsilon_squared": max(float(epsilon_squared), 0.0),
    }


def benjamini_hochberg(p_values: pd.Series) -> pd.Series:
    p_values = pd.to_numeric(p_values, errors="coerce")
    adjusted = pd.Series(np.nan, index=p_values.index, dtype="float64")
    valid = p_values.dropna().sort_values()
    n = len(valid)

    if n == 0:
        return adjusted

    ranked = valid * n / np.arange(1, n + 1)
    ranked = ranked.iloc[::-1].cummin().iloc[::-1].clip(upper=1)
    adjusted.loc[ranked.index] = ranked
    return adjusted


def calculate_vif(
    df: pd.DataFrame,
    columns: list[str],
    sample_size: int = 50_000,
    random_state: int = 42,
) -> pd.DataFrame:
    data = df[columns].apply(pd.to_numeric, errors="coerce")
    data = data.dropna(axis=1, how="all")
    data = data.fillna(data.median(numeric_only=True))
    data = data.replace([np.inf, -np.inf], np.nan).fillna(data.median(numeric_only=True))

    if len(data) > sample_size:
        data = data.sample(sample_size, random_state=random_state)

    rows = []
    usable_columns = data.columns.tolist()

    for col in usable_columns:
        other_cols = [candidate for candidate in usable_columns if candidate != col]
        if not other_cols:
            continue

        y = data[col].to_numpy()
        x = data[other_cols].to_numpy()
        model = LinearRegression()
        model.fit(x, y)
        r2 = model.score(x, y)
        vif = np.inf if r2 >= 0.999999 else 1 / (1 - r2)
        rows.append({"feature": col, "r2": r2, "vif": vif})

    return pd.DataFrame(rows).sort_values("vif", ascending=False).reset_index(drop=True)
