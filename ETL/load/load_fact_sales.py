from pathlib import Path

import pandas as pd
from sqlalchemy import Date, Integer, Float
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert

from DB.db_config import engine
from models.fact_sales import FactSales


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# =========================================================
# LOAD FACT SALES CSV
# =========================================================

def load_fact_sales_csv():

    fact_sales_path = PROCESSED_DIR / "fact_sales.csv"

    if not fact_sales_path.exists():
        raise FileNotFoundError(
            f"fact_sales.csv not found: {fact_sales_path}"
        )

    print(f"Loading: {fact_sales_path}")

    fact_sales = pd.read_csv(
        fact_sales_path
    )

    print(
        f"Loaded {len(fact_sales)} records "
        f"with {len(fact_sales.columns)} columns"
    )

    return fact_sales


# =========================================================
# PREPARE DATA
# =========================================================

def get_model_columns_by_type(model, sql_types):
    """
    Return the model's column names whose SQL type matches
    sql_types. Deriving this from the model (instead of a
    hand-maintained list) means it can never fall out of sync
    with the schema - e.g. a new Date column added to the model
    is picked up automatically instead of silently being left
    as a raw string.
    """

    return [
        column.name
        for column in model.__table__.columns
        if isinstance(column.type, sql_types)
    ]


def prepare_fact_sales(fact_sales):

    # -----------------------------------------------------
    # Date columns (derived from the model)
    # -----------------------------------------------------

    date_columns = get_model_columns_by_type(FactSales, Date)

    for column in date_columns:

        if column in fact_sales.columns:

            fact_sales[column] = (
                pd.to_datetime(
                    fact_sales[column],
                    errors="coerce"
                ).dt.date
            )

    # -----------------------------------------------------
    # Numeric columns (derived from the model)
    # -----------------------------------------------------

    numeric_columns = get_model_columns_by_type(
        FactSales,
        (Integer, Float)
    )

    for column in numeric_columns:

        if column in fact_sales.columns:

            fact_sales[column] = pd.to_numeric(
                fact_sales[column],
                errors="coerce"
            )

    # -----------------------------------------------------
    # Shipping method
    # -----------------------------------------------------

    if "shipping_method" in fact_sales.columns:

        fact_sales["shipping_method"] = (
            fact_sales["shipping_method"]
            .fillna("Unknown")
        )

    # -----------------------------------------------------
    # Refund
    # -----------------------------------------------------

    if "refund_amount" in fact_sales.columns:

        fact_sales["refund_amount"] = (
            fact_sales["refund_amount"]
            .fillna(0)
        )

    # -----------------------------------------------------
    # Return status
    # -----------------------------------------------------

    if "return_status" in fact_sales.columns:

        fact_sales["return_status"] = (
            fact_sales["return_status"]
            .fillna("Not Returned")
        )

    # -----------------------------------------------------
    # Replace NaN with None
    # -----------------------------------------------------

    fact_sales = (
        fact_sales
        .astype(object)
        .where(
            pd.notna(fact_sales),
            None
        )
    )

    return fact_sales


# =========================================================
# VALIDATE AND SELECT MODEL COLUMNS
# =========================================================
def validate_fact_sales_columns(fact_sales):

    # -----------------------------------------------------
    # Get columns from SQLAlchemy model
    # -----------------------------------------------------

    model_columns = [
        column.name
        for column in FactSales.__table__.columns
    ]

    csv_columns = set(fact_sales.columns)

    model_column_set = set(model_columns)

    # -----------------------------------------------------
    # Extra CSV columns
    # -----------------------------------------------------

    extra_columns = csv_columns - model_column_set

    if extra_columns:

        print(
            "\nWARNING: Extra CSV columns detected:"
        )

        print(
            sorted(extra_columns)
        )

        print(
            "\nThese columns will be ignored."
        )

    # -----------------------------------------------------
    # Add missing model columns
    # -----------------------------------------------------

    missing_columns = model_column_set - csv_columns

    if missing_columns:

        print(
            "\nWARNING: Model columns missing "
            "from CSV:"
        )

        print(
            sorted(missing_columns)
        )

        print(
            "\nAdding missing columns with None..."
        )

        for column in missing_columns:

            fact_sales[column] = None

    # -----------------------------------------------------
    # Obsolete refund column check
    # -----------------------------------------------------

    if "return_refund_amount" in csv_columns:

        raise ValueError(
            "Old column 'return_refund_amount' "
            "still exists in fact_sales.csv. "
            "Regenerate fact_sales.csv."
        )

    if "return_refund_amount" in model_column_set:

        raise ValueError(
            "Old column 'return_refund_amount' "
            "still exists in FactSales model."
        )

    # -----------------------------------------------------
    # Keep ONLY model columns
    # -----------------------------------------------------

    fact_sales = fact_sales[
        model_columns
    ].copy()

    print(
        "\nFact sales column validation completed."
    )

    print(
        f"Columns going to database: "
        f"{len(fact_sales.columns)}"
    )

    return fact_sales


# =========================================================
# VALIDATE NOT-NULL COLUMNS BEFORE INSERT
# =========================================================

def validate_not_null_columns(fact_sales):
    """
    Check every NOT NULL column on the FactSales model for
    None/NaN values before hitting the database. Failing here
    gives a clear, actionable message (which columns, how many
    rows) instead of a raw MySQL IntegrityError deep inside
    the upsert.
    """

    not_null_columns = [
        column.name
        for column in FactSales.__table__.columns
        if not column.nullable
    ]

    null_report = {}

    for column in not_null_columns:

        if column not in fact_sales.columns:
            continue

        null_count = int(fact_sales[column].isna().sum())

        if null_count > 0:
            null_report[column] = null_count

    if null_report:

        raise ValueError(
            "fact_sales.csv has NULL values in NOT NULL "
            f"columns: {null_report}. Regenerate fact_sales.csv "
            "via transformation_pipeline.py - the bad rows must "
            "be fixed upstream, not patched here."
        )

    print("NOT NULL validation passed.")


# =========================================================
# UPSERT FACT SALES
# =========================================================

def upsert_fact_sales(fact_sales):

    records = fact_sales.to_dict(
        orient="records"
    )

    if not records:

        print(
            "No records found."
        )

        return

    chunk_size = 5000

    with Session(engine) as session:

        for start in range(
            0,
            len(records),
            chunk_size
        ):

            chunk = records[
                start:start + chunk_size
            ]

            # -------------------------------------------------
            # INSERT
            # -------------------------------------------------

            stmt = insert(
                FactSales
            ).values(
                chunk
            )

            # -------------------------------------------------
            # UPDATE ON DUPLICATE KEY
            # -------------------------------------------------

            update_columns = {
                column.name: stmt.inserted[column.name]
                for column in FactSales.__table__.columns
                if column.name != "order_item_id"
            }

            stmt = stmt.on_duplicate_key_update(
                **update_columns
            )

            session.execute(
                stmt
            )

            processed = min(
                start + chunk_size,
                len(records)
            )

            print(
                f"Processed "
                f"{processed} / "
                f"{len(records)} records"
            )

        session.commit()

    print(
        "\nfact_sales upsert completed successfully."
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    try:

        print(
            "\n" + "=" * 70
        )

        print(
            "STARTING FACT SALES LOAD"
        )

        print(
            "=" * 70
        )

        # -----------------------------------------------------
        # 1. Load CSV
        # -----------------------------------------------------

        fact_sales = load_fact_sales_csv()

        # -----------------------------------------------------
        # 2. Validate and select model columns
        # -----------------------------------------------------

        fact_sales = validate_fact_sales_columns(
            fact_sales
        )

        # -----------------------------------------------------
        # 3. Prepare data
        # -----------------------------------------------------

        fact_sales = prepare_fact_sales(
            fact_sales
        )

        # -----------------------------------------------------
        # 3b. Validate NOT NULL columns
        # -----------------------------------------------------

        validate_not_null_columns(
            fact_sales
        )

        # -----------------------------------------------------
        # 4. Upsert into MySQL
        # -----------------------------------------------------

        upsert_fact_sales(
            fact_sales
        )

        print(
            "\n" + "=" * 70
        )

        print(
            "FACT SALES LOAD COMPLETED"
        )

        print(
            "=" * 70
        )

    except Exception as e:

        print(
            "\nError loading fact_sales:"
        )

        print(e)

        raise