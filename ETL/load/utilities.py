from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

def read_processed_csv(filename: str) -> pd.DataFrame:
    """
    Read a processed CSV file.
    """

    file_path = PROCESSED_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed file not found: {file_path}"
        )

    print(f"Reading: {file_path}")

    return pd.read_csv(file_path)


def select_existing_columns(
    df: pd.DataFrame,
    columns: list[str]
) -> pd.DataFrame:
    """
    Select only columns that exist in the dataframe.
    """

    existing_columns = [
        column
        for column in columns
        if column in df.columns
    ]

    return df[existing_columns].copy()


def execute_sql(sql: str) -> None:
    """
    Execute a SQL statement.
    """

    with engine.begin() as connection:
        connection.execute(text(sql))
