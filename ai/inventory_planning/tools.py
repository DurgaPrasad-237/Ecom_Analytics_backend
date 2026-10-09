from pathlib import Path

from analytics.customer_analytics.data_loader import load_customer_data

from analytics.InventoryPlanning.analysis import (
    load_products,
    get_inventory_demand_by_product,
    get_inventory_position,
    get_inventory_products
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INVENTORY_PLANNING_PATH = (
    BASE_DIR
    / "ML"
    / "inventory_planning"
    / "results"
    / "inventory_plan_2026.csv"
)

PRODUCTS_PLANNING_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "products_processed.csv"
)

FORECAST_PATH = (
    BASE_DIR
    /"ML"
    /"DemandForecasting"
    /"results"
    /"2026_demand_forecast.csv"
)

df = load_customer_data(INVENTORY_PLANNING_PATH)
products_df = load_customer_data(PRODUCTS_PLANNING_PATH)
forecast_df = load_customer_data(FORECAST_PATH)
final_df = df.merge(
    products_df[["product_name","stock_quantity"]],
    how="left",
    on="product_name"

)


# ============================================================
# INVENTORY PLANNING FUNCTIONS
# ============================================================

def inventory_products():

   

    return load_products(final_df)


def inventory_demand_by_product(
    product_name: str
):

    return get_inventory_demand_by_product(
        final_df,
        product_name
    )


def inventory_position(
    product_name: str,
    lead_time_days: int = 7
):

    

    return get_inventory_position(
        final_df,
        forecast_df,
        product_name,
        lead_time_days
    )


def inventory_products_table(
    page: int = 1,
    page_size: int = 10,
    stock_filter: str = "all",
    search: str = ""
):

   

    return get_inventory_products(
        final_df,
        page=page,
        page_size=page_size,
        stock_filter=stock_filter,
        search=search
    )


# ============================================================
# TOOL REGISTRY
# ============================================================

INVENTORY_PLANNING_TOOL_FUNCTIONS = {

    "inventory_products":
        inventory_products,

    "inventory_demand_by_product":
        inventory_demand_by_product,

    "inventory_position":
        inventory_position,

    "inventory_products_table":
        inventory_products_table,

}


# ============================================================
# OPENAI TOOL DEFINITIONS
# ============================================================

INVENTORY_PLANNING_TOOLS = [
    {
        "type": "function",
        "name": "inventory_products",
        "description": "Get the list of available product names in the inventory planning data.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "inventory_demand_by_product",
        "description": (
            "Get inventory planning metrics for a specific product, "
            "including total forecast demand, average daily demand, "
            "maximum daily demand, lead-time demand, safety stock, "
            "reorder point, recommended inventory, and current stock."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Exact product name."
                }
            },
            "required": ["product_name"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "inventory_position",
        "description": (
            "Get the expected inventory position for a specific product "
            "during the supplier lead-time period."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "Exact product name."
                },
                "lead_time_days": {
                    "type": "integer",
                    "description": "Number of supplier lead-time days."
                }
            },
            "required": [
                "product_name",
                "lead_time_days"
            ],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "inventory_products_table",
        "description": (
            "Get inventory planning information for products with "
            "optional search, stock-status filtering, and pagination."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "page": {
                    "type": "integer",
                    "description": "Page number."
                },
                "page_size": {
                    "type": "integer",
                    "description": "Number of products per page."
                },
                "stock_filter": {
                    "type": "string",
                    "enum": [
                        "all",
                        "healthy",
                        "reorder",
                        "critical"
                    ],
                    "description": "Inventory stock status filter."
                },
                "search": {
                    "type": "string",
                    "description": "Optional product name search."
                }
            },
            "required": [
                "page",
                "page_size",
                "stock_filter",
                "search"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
]