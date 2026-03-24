import pandas as pd
import numpy as np

INVALID_PLACEHOLDERS = {"ERROR", "UNKNOWN"}


def _replace_invalids_with_nan(series: pd.Series) -> pd.Series:
    return series.replace(INVALID_PLACEHOLDERS, np.nan)


def _clean_numeric(series: pd.Series) -> pd.Series:
    series = _replace_invalids_with_nan(series)
    return pd.to_numeric(series, errors="coerce")


def _clean_categorical(series: pd.Series) -> pd.Series:
    series = _replace_invalids_with_nan(series)
    return series.str.strip()


def _clean_date(series: pd.Series) -> pd.Series:
    series = _replace_invalids_with_nan(series)
    return pd.to_datetime(series, errors="coerce")


def _clean_id(series: pd.Series) -> pd.Series:
    return series.str.strip()


def clean_dataframe(df: pd.DataFrame, column_types: dict, derived_columns: list[dict] | None = None) -> tuple[pd.DataFrame, dict]:
    """
    Clean each column based on its detected type.
    Returns cleaned DataFrame and a stats dict of what was fixed.
    """
    df = df.copy()
    fix_stats = {}

    for col, col_type in column_types.items():
        original = df[col].copy()

        if col_type == "numeric":
            df[col] = _clean_numeric(df[col])
        elif col_type == "categorical":
            df[col] = _clean_categorical(df[col])
        elif col_type == "date":
            df[col] = _clean_date(df[col])
        elif col_type == "id":
            df[col] = _clean_id(df[col])

        fixed = int(original.notna().sum()) - int(
            original[original == df[col]].notna().sum()
        )
        fix_stats[col] = {
            "type": col_type,
            "null_before": int(original.isna().sum()),
            "null_after": int(df[col].isna().sum()),
        }

    if derived_columns:
        for rule in derived_columns:
            target = rule["target"]
            factors = rule["factors"]
            if target in df.columns and all(f in df.columns for f in factors):
                mask = df[target].isna()
                for f in factors:
                    mask = mask & df[f].notna()
                df.loc[mask, target] = df.loc[mask, factors].prod(axis=1)

    df = df.drop_duplicates()

    return df, fix_stats
