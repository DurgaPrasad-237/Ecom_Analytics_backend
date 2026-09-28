from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select

from DB.db_config import engine
from models.dim_products import DimProduct
from sqlalchemy.dialects.mysql import insert

# =========================================================
# Project Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"


# =========================================================
# Load Product Dimension
# =========================================================

def load_dim_products():

    file_path = PROCESSED_DIR / "products_processed.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    print(f"Loading: {file_path}")

    df_products = pd.read_csv(file_path)

    # Select only the columns required by dim_product
    df_product = df_products[
        [
            "product_id",
            "product_name",
            "category",
            "subcategory",
            "brand",
            "price",
            "cost_price",
            "discount_range",
            "rating_average",
            "rating_count",
            "stock_quantity",
            "product_launch_date",
            "product_type",
            "return_rate_baseline",
        ]
    ].copy()

    # Convert date column
    df_product["product_launch_date"] = pd.to_datetime(
        df_product["product_launch_date"]
    ).dt.date

    # Convert DataFrame rows into SQLAlchemy objects
    records = []

    for _, row in df_product.iterrows():

        product_record = DimProduct(
            product_id=row["product_id"],
            product_name=row["product_name"],
            category=row["category"],
            subcategory=row["subcategory"],
            brand=row["brand"],
            price=row["price"],
            cost_price=row["cost_price"],
            discount_range=row["discount_range"],
            rating_average=row["rating_average"],
            rating_count=row["rating_count"],
            stock_quantity=row["stock_quantity"],
            product_launch_date=row["product_launch_date"],
            product_type=row["product_type"],
            return_rate_baseline=row["return_rate_baseline"],
        )

        records.append(product_record)


    # Insert only new records into MySQL
    with Session(engine) as session:

        values = [
            {
                "product_id": record.product_id,
                "product_name": record.product_name,
                "category": record.category,
                "subcategory": record.subcategory,
                "brand": record.brand,
                "price": record.price,
                "cost_price": record.cost_price,
                "discount_range": record.discount_range,
                "rating_average": record.rating_average,
                "rating_count": record.rating_count,
                "stock_quantity": record.stock_quantity,
                "product_launch_date": record.product_launch_date,
                "product_type": record.product_type,
                "return_rate_baseline": record.return_rate_baseline,
            }
            for record in records
        ]

        stmt = insert(DimProduct).values(values)

        stmt = stmt.on_duplicate_key_update(
            product_name=stmt.inserted.product_name,
            category=stmt.inserted.category,
            subcategory=stmt.inserted.subcategory,
            brand=stmt.inserted.brand,
            price=stmt.inserted.price,
            cost_price=stmt.inserted.cost_price,
            discount_range=stmt.inserted.discount_range,
            rating_average=stmt.inserted.rating_average,
            rating_count=stmt.inserted.rating_count,
            stock_quantity=stmt.inserted.stock_quantity,
            product_launch_date=stmt.inserted.product_launch_date,
            product_type=stmt.inserted.product_type,
            return_rate_baseline=stmt.inserted.return_rate_baseline,
        )

        session.execute(stmt)
        session.commit()

    print("Product dimension upsert completed successfully.")


# =========================================================
# Entry Point
# =========================================================

if __name__ == "__main__":
    load_dim_products()