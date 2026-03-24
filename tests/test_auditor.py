import pandas as pd

from src.auditor import audit_column, audit_dataframe


def test_audit_counts_nulls():
    series = pd.Series(["Coffee", None, "Tea", None, "ERROR"])

    result = audit_column(series, col_type="categorical")

    assert result["null_count"] == 2


def test_audit_counts_invalid_placeholders():
    series = pd.Series(["Coffee", "ERROR", "UNKNOWN", "Tea", None])

    result = audit_column(series, col_type="categorical")

    assert result["invalid_placeholder_count"] == 2


def test_audit_numeric_non_numeric_count():
    series = pd.Series(["1.0", "2.0", "abc", "ERROR", None])

    result = audit_column(series, col_type="numeric")

    assert result["non_numeric_count"] == 1


def test_audit_date_unparseable_count():
    series = pd.Series(["2023-01-01", "not-a-date", "ERROR", None])

    result = audit_column(series, col_type="date")

    assert result["unparseable_date_count"] == 1


def test_audit_dataframe():
    df = pd.DataFrame(
        {
            "item": ["Coffee", "ERROR", None],
            "quantity": ["1", "UNKNOWN", None],
        }
    )
    column_types = {"item": "categorical", "quantity": "numeric"}

    result = audit_dataframe(df, column_types)

    assert "item" in result
    assert "quantity" in result
