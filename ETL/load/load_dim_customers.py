from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from DB.db_config import engine
from models.dim_customers import DimCustomer
from sqlalchemy.dialects.mysql import insert

# =========================================================
# Project Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# =========================================================
# Load Customer Dimension
# =========================================================

def load_dim_customer():

    file_path = PROCESSED_DIR / "customers_processed.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    print(f"Loading: {file_path}")

    df_customer = pd.read_csv(file_path)

    # Convert date columns back to datetime after reading CSV
    df_customer["customer_signup_date"] = pd.to_datetime(
        df_customer["customer_signup_date"]
    )

    df_customer["last_order_date"] = pd.to_datetime(
        df_customer["last_order_date"]
    )

    

    # Select only columns required by dim_customer
    df_customer = df_customer[
        [
            "customer_id",
            "customer_signup_date",
            "gender",
            "age",
            "age_group",
            "state",
            "city",
            "customer_segment",
            "preferred_device",
            "preferred_payment_method",
            "acquisition_channel",
            "total_orders",
            "total_spend",
            "last_order_date",
            "average_order_value",
            "customer_status",
            "loyalty_tier"
        ]
    ].copy()



    # Remove duplicate customer records
    df_customer = df_customer.drop_duplicates(
        subset=["customer_id"]
    )

    # handling NaT value for last_order_date
    df_customer["last_order_date"] = df_customer["last_order_date"].apply(
        lambda x: x.date() if pd.notna(x) else None
    )


    # Convert DataFrame into dictionaries
    records = df_customer.to_dict(orient="records")

    # MySQL INSERT statement
    stmt = insert(DimCustomer).values(records)

    # If customer_id already exists → UPDATE
    update_columns = {
        "customer_signup_date": stmt.inserted.customer_signup_date,
        "gender": stmt.inserted.gender,
        "age": stmt.inserted.age,
        "age_group": stmt.inserted.age_group,
        "state": stmt.inserted.state,
        "city": stmt.inserted.city,
        "customer_segment": stmt.inserted.customer_segment,
        "preferred_device": stmt.inserted.preferred_device,
        "preferred_payment_method": stmt.inserted.preferred_payment_method,
        "acquisition_channel": stmt.inserted.acquisition_channel,
        "total_orders": stmt.inserted.total_orders,
        "total_spend": stmt.inserted.total_spend,
        "last_order_date": stmt.inserted.last_order_date,
        "average_order_value": stmt.inserted.average_order_value,
        "customer_status": stmt.inserted.customer_status,
        "loyalty_tier": stmt.inserted.loyalty_tier,
    }

    stmt = stmt.on_duplicate_key_update(**update_columns)

   
    # Execute upsert
    with Session(engine) as session:
        session.execute(stmt)
        session.commit()


    print(
        f"{len(records)} customer records upserted successfully"
    )


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":
    load_dim_customer()