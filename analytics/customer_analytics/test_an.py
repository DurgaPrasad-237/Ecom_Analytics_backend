from pathlib import Path
from analytics.customer_analytics.analysis import total_customers_by_gender
from analytics.customer_analytics.data_loader import load_customer_data
BASE_DIR = Path(__file__).resolve().parent.parent.parent


CUSTOMER_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "customers_processed.csv"
)

print(total_customers_by_gender(load_customer_data(CUSTOMER_FILEPATH)))