from pathlib import Path

from analytics.sales_analytics.analysis import sales_kpis
from analytics.sales_analytics.data_loader import load_order_items_data


BASE_DIR = Path(__file__).resolve().parent.parent.parent

ORDER_ITEMS_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "order_items_processed.csv"
)


def get_sales_kpis():
    oi_df = load_order_items_data(ORDER_ITEMS_FILEPATH)
    return sales_kpis(oi_df)


SALES_TOOL_FUNCTIONS = {
    "get_sales_kpis": get_sales_kpis,
}


SALES_TOOLS = [
    {
        "type": "function",
        "name": "get_sales_kpis",
        "description": (
            "Get sales KPIs including gross revenue, gross profit, "
            "profit margin, refund amount, net revenue, and total item cost."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        "strict": True,
    }
]