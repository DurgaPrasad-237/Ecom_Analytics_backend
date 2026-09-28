from pathlib import Path

from analytics.product_analytics.analysis import (
    total_number_of_unitsSold,
)
from analytics.product_analytics.data_loader import load_productS_data

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ============================================================
# PRODUCT DATA
# ============================================================

# Use the same dataframe that your FastAPI product analytics uses.
PRODUCT_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "products_processed.csv"
)




# ============================================================
# PRODUCT ANALYTICS FUNCTIONS
# ============================================================

def total_units_sold():
    f_df = load_productS_data(PRODUCT_FILEPATH)
    return total_number_of_unitsSold(f_df)


# ============================================================
# TOOL REGISTRY
# ============================================================

PRODUCT_TOOL_FUNCTIONS = {

    "total_units_sold":
        total_units_sold,

   

}


# ============================================================
# OPENAI TOOL DEFINITIONS
# ============================================================

PRODUCT_TOOLS = [

    {
        "type": "function",
        "name": "total_units_sold",
        "description": (
            "Get the total number of units sold."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    }

]