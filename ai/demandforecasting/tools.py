from pathlib import Path

from analytics.customer_analytics.data_loader import load_customer_data

from analytics.DemandForecasting.analysis import (
    get_forecast_kpis,
    get_product_forecast,
    get_top_products
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent


FORECAST_FILEPATH = (
    BASE_DIR
    / "ML"
    / "DemandForecasting"
    / "results"
    / "2026_demand_forecast.csv"
)


# ============================================================
# DATA LOADER
# ============================================================

def get_forecast_data():

    return load_customer_data(
        FORECAST_FILEPATH
    )


# ============================================================
# DEMAND FORECASTING FUNCTIONS
# ============================================================

def forecast_kpis(
    from_date: str,
    to_date: str,
    product_name: str = None
):

    df = get_forecast_data()

    return get_forecast_kpis(
        df,
        from_date,
        to_date,
        product_name
    )


def product_forecast(
    from_date: str,
    to_date: str,
    product_name: str
):

    df = get_forecast_data()

    return get_product_forecast(
        df,
        from_date,
        to_date,
        product_name
    )


def top_forecast_products(
    from_date: str,
    to_date: str
):

    df = get_forecast_data()

    return get_top_products(
        df,
        from_date,
        to_date
    )


# ============================================================
# TOOL REGISTRY
# ============================================================

DEMAND_FORECASTING_TOOL_FUNCTIONS = {

    "forecast_kpis":
        forecast_kpis,

    "product_forecast":
        product_forecast,

    "top_forecast_products":
        top_forecast_products,

}


# ============================================================
# OPENAI TOOL DEFINITIONS
# ============================================================

DEMAND_FORECASTING_TOOLS = [

    {
        "type": "function",
        "name": "forecast_kpis",
        "description": (
            "Get demand forecasting KPIs for a specified date range. "
            "Returns total forecasted demand, average daily demand, "
            "and peak daily demand. A product can optionally be specified."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "from_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format."
                },
                "to_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format."
                },
                "product_name": {
                    "type": ["string", "null"],
                    "description": (
                        "Optional product name. Use null when calculating "
                        "KPIs for all products."
                    )
                }
            },
            "required": [
                "from_date",
                "to_date",
                "product_name"
            ],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "product_forecast",
        "description": (
            "Get daily demand forecast values for a specific product "
            "within a specified date range."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "from_date": {
                    "type": "string",
                    "description": (
                        "Start date of the forecast period "
                        "in YYYY-MM-DD format."
                    )
                },
                "to_date": {
                    "type": "string",
                    "description": (
                        "End date of the forecast period "
                        "in YYYY-MM-DD format."
                    )
                },
                "product_name": {
                    "type": "string",
                    "description": (
                        "Exact product name for which the "
                        "forecast is required."
                    )
                }
            },
            "required": [
                "from_date",
                "to_date",
                "product_name"
            ],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "top_forecast_products",
        "description": (
            "Get the top 10 products with the highest total "
            "forecasted demand within a specified date range."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "from_date": {
                    "type": "string",
                    "description": (
                        "Start date of the forecast period "
                        "in YYYY-MM-DD format."
                    )
                },
                "to_date": {
                    "type": "string",
                    "description": (
                        "End date of the forecast period "
                        "in YYYY-MM-DD format."
                    )
                }
            },
            "required": [
                "from_date",
                "to_date"
            ],
            "additionalProperties": False
        },
        "strict": True
    }

]