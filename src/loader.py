import pandas as pd


def load_raw(filepath: str) -> pd.DataFrame:
    """Load CSV as all strings to preserve dirty values exactly as-is."""
    df = pd.read_csv(filepath, dtype=str)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df