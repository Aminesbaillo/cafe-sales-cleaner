import numpy as np
import pandas as pd

from src.cleaner import clean_dataframe


def test_cleans_numeric_column():
    df = pd.DataFrame({"quantity": ["1", "2", "ERROR", "UNKNOWN", None]})
    column_types = {"quantity": "numeric"}

    cleaned_df, _ = clean_dataframe(df, column_types)

    assert cleaned_df["quantity"].dtype == float
    assert not cleaned_df["quantity"].isin(["ERROR", "UNKNOWN"]).any()


def test_cleans_categorical_column():
    df = pd.DataFrame({"item": ["Coffee", "ERROR", "UNKNOWN", None, "Tea"]})
    column_types = {"item": "categorical"}

    cleaned_df, _ = clean_dataframe(df, column_types)

    assert not cleaned_df["item"].isin(["ERROR", "UNKNOWN"]).any()
    assert set(cleaned_df["item"].dropna().unique()) == {"Coffee", "Tea"}


def test_cleans_date_column():
    df = pd.DataFrame({"transaction_date": ["2023-01-01", "ERROR", None]})
    column_types = {"transaction_date": "date"}

    cleaned_df, _ = clean_dataframe(df, column_types)

    assert not cleaned_df["transaction_date"].isin(["ERROR"]).any()
    assert cleaned_df["transaction_date"].notna().sum() == 1


def test_recalculates_total_spent():
    df = pd.DataFrame(
        {
            "quantity": [2.0, 3.0],
            "price_per_unit": [5.0, 4.0],
            "total_spent": [np.nan, 12.0],
        }
    )
    column_types = {
        "quantity": "numeric",
        "price_per_unit": "numeric",
        "total_spent": "numeric",
    }
    derived_columns = [{"target": "total_spent", "factors": ["quantity", "price_per_unit"]}]

    cleaned_df, _ = clean_dataframe(df, column_types, derived_columns=derived_columns)

    assert cleaned_df.loc[0, "total_spent"] == 10.0


def test_removes_duplicates():
    df = pd.DataFrame({"item": ["Coffee", "Coffee"], "quantity": ["1", "1"]})
    column_types = {"item": "categorical", "quantity": "numeric"}

    cleaned_df, _ = clean_dataframe(df, column_types)

    assert len(cleaned_df) == 1
