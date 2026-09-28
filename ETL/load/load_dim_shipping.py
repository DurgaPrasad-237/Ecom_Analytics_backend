from pathlib import Path

import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert

from DB.db_config import engine
from models.dim_shipments import DimShipping


# =========================================================
# Project Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# =========================================================
# Load Shipping Dimension
# =========================================================

def load_dim_shipping():

    file_path = PROCESSED_DIR / "shipments_processed.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    print(f"Loading: {file_path}")

    df_shipments = pd.read_csv(file_path)

    # Select only the columns required by dim_shipping
    df_shipping = df_shipments[
        [
            "shipment_id",
            "shipping_method",
            "warehouse_city",
            "delivery_city",
        ]
    ].copy()

    # Convert DataFrame rows into dictionaries
    records = df_shipping.to_dict(
        orient="records"
    )

    if not records:
        print("No shipping records found.")
        return

    # =====================================================
    # Upsert records into MySQL
    # =====================================================

    with Session(engine) as session:

        stmt = insert(DimShipping).values(
            records
        )

        stmt = stmt.on_duplicate_key_update(
            shipping_method=stmt.inserted.shipping_method,
            warehouse_city=stmt.inserted.warehouse_city,
            delivery_city=stmt.inserted.delivery_city,
        )

        session.execute(stmt)

        session.commit()

    print(
        f"{len(records)} shipping records "
        f"upserted successfully"
    )


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":

    try:

        load_dim_shipping()

    except Exception as e:

        print(
            "Error loading dim_shipping:",
            e
        )