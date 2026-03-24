import pandas as pd

INVALID_PLACEHOLDERS = {"ERROR", "UNKNOWN"}
DATE_KEYWORDS = ["date", "time", "day"]
ID_KEYWORDS = ["id"]


def _clean_series(series: pd.Series) -> pd.Series:
    """Return series with NaN and invalid placeholders removed."""
    return series[~series.isin(INVALID_PLACEHOLDERS) & series.notna()]


def _is_id_column(col_name: str) -> bool:
    return any(kw in col_name.lower() for kw in ID_KEYWORDS)


def _is_date_column(col_name: str, series: pd.Series) -> bool:
    if any(kw in col_name.lower() for kw in DATE_KEYWORDS):
        return True
    sample = _clean_series(series).head(20)
    COMMON_DATE_FORMATS = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%m-%d-%Y",
    ]
    for fmt in COMMON_DATE_FORMATS:
        try:
            pd.to_datetime(sample, format=fmt, errors="raise")
            return True
        except Exception:
            continue
    return False


def _is_numeric_column(series: pd.Series) -> bool:
    clean = _clean_series(series)
    if len(clean) == 0:
        return False
    numeric_count = pd.to_numeric(clean, errors="coerce").notna().sum()
    return (numeric_count / len(clean)) >= 0.8


def _is_categorical_column(series: pd.Series) -> bool:
    clean = _clean_series(series)
    if len(clean) == 0:
        return False
    return (clean.nunique() / len(clean)) < 0.05


def detect_column_types(df: pd.DataFrame) -> dict:
    """
    Returns a dict mapping each column name to one of:
    'id', 'date', 'numeric', 'categorical', 'text'
    """
    column_types = {}
    for col in df.columns:
        series = df[col]
        if _is_id_column(col):
            column_types[col] = "id"
        elif _is_date_column(col, series):
            column_types[col] = "date"
        elif _is_numeric_column(series):
            column_types[col] = "numeric"
        elif _is_categorical_column(series):
            column_types[col] = "categorical"
        else:
            column_types[col] = "text"
    return column_types
