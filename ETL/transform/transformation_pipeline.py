from pathlib import Path

import pandas as pd

from ETL.transform.cleaning import (
    handle_missing_values,
    fix_data_types,
    
)

from ETL.transform.feature_engineering import *

from ETL.transform.validation import validate_data



# =========================================================
# Project Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# Load CSV Files
# =========================================================

def load_csv(filename: str) -> pd.DataFrame:
    """
    Load one CSV file from the raw data directory.
    """

    file_path = RAW_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    print(f"Loading: {file_path}")

    return pd.read_csv(file_path)

# =======================================================
# create fact sales
# =======================================================
def create_fact_sales(
   
):
    pass


# =========================================================
# Save CSV Files
# =========================================================

def save_csv(
    df: pd.DataFrame,
    filename: str
) -> None:
    """
    Save dataframe into the processed directory.
    """

    output_path = PROCESSED_DIR / filename

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved: {output_path} | "
        f"Rows: {len(df)} | "
        f"Columns: {len(df.columns)}"
    )


# =========================================================
# Main Transformation Pipeline
# =========================================================

def main():

    print("\n" + "=" * 70)
    print("STARTING ETL TRANSFORMATION PIPELINE")
    print("=" * 70)

    # -----------------------------------------------------
    # 1. Load all raw CSV files
    # -----------------------------------------------------

    df_customer = load_csv("customers.csv")

    df_customer_reviews = load_csv(
        "customer_reviews.csv"
    )

    df_orders = load_csv("orders.csv")

    df_order_items = load_csv(
        "order_items.csv"
    )

    df_products = load_csv("products.csv")

    df_payments = load_csv("payments.csv")

    df_returns = load_csv("returns.csv")

    df_shipments = load_csv("shipments.csv")

    # -----------------------------------------------------
    # 2. Fix data types
    # -----------------------------------------------------

    print("\nFixing data types...")

    (
        df_customer,
        df_customer_reviews,
        df_orders,
        df_products,
        df_shipments
    ) = fix_data_types(
        df_customer,
        df_customer_reviews,
        df_orders,
        df_products,
        df_shipments
    )

    # -----------------------------------------------------
    # 3. Handle missing values
    # -----------------------------------------------------

    print("\nHandling missing values...")

    (
        df_customer,
        df_customer_reviews,
        df_orders,
        df_products,
        df_shipments
    ) = handle_missing_values(
        df_customer,
        df_customer_reviews,
        df_orders,
        df_products,
        df_shipments
    )

    # -----------------------------------------------------
    # 4. Feature engineering
    # -----------------------------------------------------

    print("\nCreating features...")

    df_orders = orders_table(df_orders)
    df_customer = customer_signup_month(df_customer)
    df_customer = customer_signup_year(df_customer)
    df_order_items = enrich_order_items_with_returns(df_order_items,df_returns)
    df_products = calculate_units_sold_per_product(df_order_items,df_products)
    df_products = calculate_returned_units_per_product(df_order_items,df_products)
    df_products = calculate_product_return_rate(df_products)


    # -----------------------------------------------------
    # 5. Validation
    # -----------------------------------------------------

    print("\nRunning validation...")

    validate_data(
        df_customer=df_customer,
        df_customer_review=df_customer_reviews,
        df_orders=df_orders,
        df_order_items=df_order_items,
        df_products=df_products,
        df_payments=df_payments,
        df_returns=df_returns,
        df_shipments=df_shipments
    )

    # ----------------------------------------------------
    #  6. create fact sales
    # ----------------------------------------------------
    # df_fact_sales = create_fact_sales(
    #     df_orders=df_orders,
    #     df_order_items=df_order_items,
    #     df_products=df_products,
    #     df_customers=df_customer,
    #     df_payments=df_payments,
    #     df_returns=df_returns,
    #     df_cust_rev=df_customer_reviews,
    #     df_shipments=df_shipments
    # )


    # -----------------------------------------------------
    # 7. Save processed detailed datasets
    # -----------------------------------------------------

    print("\nSaving processed datasets...")

    save_csv(
        df_customer,
        "customers_processed.csv"
    )

    save_csv(
        df_customer_reviews,
        "customer_reviews_processed.csv"
    )

    save_csv(
        df_orders,
        "orders_processed.csv"
    )

    save_csv(
        df_order_items,
        "order_items_processed.csv"
    )

    save_csv(
        df_products,
        "products_processed.csv"
    )

    save_csv(
        df_payments,
        "payments_processed.csv"
    )

    save_csv(
        df_returns,
        "returns_processed.csv"
    )

    save_csv(
        df_shipments,
        "shipments_processed.csv"
    )
    # save_csv(
    #      df_fact_sales,
    #      "fact_sales.csv"
    # )

  

    print("\n" + "=" * 70)
    print("ETL TRANSFORMATION PIPELINE COMPLETED")
    print("=" * 70)


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":
    main()