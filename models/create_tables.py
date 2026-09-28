from sqlalchemy import text

from DB.db_config import engine, Base

# Import models so SQLAlchemy knows about them
from models.fact_sales import FactSales
from models.dim_customers import DimCustomer
from models.dim_products import DimProduct
from models.dim_shipments import DimShipping
from models.dim_date import DimDate


try:
    with engine.begin() as connection:
        Base.metadata.create_all(connection)

    print("All tables created successfully.")

except Exception as e:
    print("Error: Table creation failed. Transaction rolled back.")
    print("Error:", e)