import pandas as pd

INVALID_PLACEHOLDERS = {"ERROR", "UNKNOWN"}


def _count_invalids(series: pd.Series) -> int:
    return series.isin(INVALID_PLACEHOLDERS).sum()


def _count_nulls(series: pd.Series) -> int:
    return series.isna().sum()


def audit_column(series: pd.Series, col_type: str) -> dict:
    """Return a problems dict for a single column based on its type."""
    problems = {
        "null_count": _count_nulls(series),
        "invalid_placeholder_count": _count_invalids(series),
    }

    if col_type == "numeric":
        clean = series[~series.isin(INVALID_PLACEHOLDERS) & series.notna()]
        non_numeric = pd.to_numeric(clean, errors="coerce").isna().sum()
        problems["non_numeric_count"] = int(non_numeric)

    if col_type == "date":
        clean = series[~series.isin(INVALID_PLACEHOLDERS) & series.notna()]
        unparseable = pd.to_datetime(clean, errors="coerce").isna().sum()
        problems["unparseable_date_count"] = int(unparseable)

    if col_type == "categorical":
        clean = series[~series.isin(INVALID_PLACEHOLDERS) & series.notna()]
        problems["unique_valid_values"] = sorted(clean.unique().tolist())

    return problems


def audit_dataframe(df: pd.DataFrame, column_types: dict) -> dict:
    """Run audit on all columns. Returns a problems dict per column."""
    return {
        col: audit_column(df[col], column_types[col])
        for col in df.columns
    }