import numpy as np
import pandas as pd

from src.detector import detect_column_types


def test_detects_id_column():
    df = pd.DataFrame(
        {"transaction_id": ["TXN_001", "TXN_002", "TXN_003"]}
    )

    column_types = detect_column_types(df)

    assert column_types["transaction_id"] == "id"


def test_detects_numeric_column():
    df = pd.DataFrame({"quantity": ["1", "2", "3", "4", "5"]})

    column_types = detect_column_types(df)

    assert column_types["quantity"] == "numeric"


def test_detects_categorical_column():
    df = pd.DataFrame(
        {"item": ["Coffee", "Tea", "Coffee", "Tea", "Coffee"] * 20}
    )

    column_types = detect_column_types(df)

    assert column_types["item"] == "categorical"


def test_detects_date_column():
    df = pd.DataFrame(
        {"purchased_on": ["2024-01-01", "2024-01-02", np.nan, "2024-01-04"]}
    )

    column_types = detect_column_types(df)

    assert column_types["purchased_on"] == "date"
