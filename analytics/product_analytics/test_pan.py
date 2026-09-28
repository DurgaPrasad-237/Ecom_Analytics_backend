from analytics.product_analytics.data_loader import load_productS_data,load_fact_sales_data
from pathlib import Path
from analytics.product_analytics.analysis import total_number_of_unitsSold

BASE_DIR = Path(__file__).resolve().parent.parent.parent

FACT_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "fact_sales.csv"
)


PRODUCT_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "products_processed.csv"
)


fact_sales = load_fact_sales_data(FACT_FILEPATH)

print(total_number_of_unitsSold(fact_sales))
