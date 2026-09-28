from datetime import timedelta
from pathlib import Path

import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert

from DB.db_config import engine
from models.dim_date import DimDate


# =========================================================
# Project Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# =========================================================
# Get Minimum and Maximum Dates
# =========================================================

def get_min_max_dates(filename: str):

    file_path = PROCESSED_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed file is not found: {file_path}"
        )

    print(f"Reading: {file_path}")

    df = pd.read_csv(file_path)

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()

    return min_date, max_date


# =========================================================
# Generate Date Records
# =========================================================

def generate_date_records(
    min_date,
    max_date
):

    records = []

    current_date = min_date
    date_id = 1

    while current_date <= max_date:

        records.append(
            {
                "date_id": date_id,
                "full_date": current_date,
                "day": current_date.day,
                "month": current_date.month,
                "month_name": current_date.strftime("%B"),
                "quarter": (
                    (current_date.month - 1) // 3 + 1
                ),
                "year": current_date.year,
                "week": current_date.isocalendar().week,
                "day_name": current_date.strftime("%A"),
            }
        )

        current_date += timedelta(days=1)
        date_id += 1

    return records


# =========================================================
# Upsert Date Dimension
# =========================================================

def load_dim_date():

    min_date, max_date = get_min_max_dates(
        "orders_processed.csv"
    )

    print(f"Minimum date: {min_date}")
    print(f"Maximum date: {max_date}")

    records = generate_date_records(
        min_date,
        max_date
    )

    if not records:
        print("No date records found.")
        return

    with Session(engine) as session:

        stmt = insert(DimDate).values(
            records
        )

        stmt = stmt.on_duplicate_key_update(

            full_date=stmt.inserted.full_date,

            day=stmt.inserted.day,

            month=stmt.inserted.month,

            month_name=stmt.inserted.month_name,

            quarter=stmt.inserted.quarter,

            year=stmt.inserted.year,

            week=stmt.inserted.week,

            day_name=stmt.inserted.day_name,
        )

        session.execute(stmt)

        session.commit()

    print(
        f"{len(records)} date records "
        f"upserted successfully"
    )


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":

    try:

        load_dim_date()

    except Exception as e:

        print(
            "Error loading dim_date:",
            e
        )