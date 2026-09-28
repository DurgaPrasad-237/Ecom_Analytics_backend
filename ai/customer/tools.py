from pathlib import Path

from analytics.customer_analytics.data_loader import load_customer_data

from analytics.customer_analytics.analysis import (
    get_monthly_signup_counts,
    get_monthly_signup_by_gender,
    get_total_customers,
    get_avg_customer_spend,
    customer_signup_yearwise_trend,
    total_customers_by_gender
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent


CUSTOMER_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "customers_processed.csv"
)


# ============================================================
# DATA LOADER
# ============================================================

def get_customer_data():

    return load_customer_data(
        CUSTOMER_FILEPATH
    )


# ============================================================
# CUSTOMER ANALYTICS FUNCTIONS
# ============================================================

def customer_signup_year_wise_trend():

    """
    Analyze customer signup trends by year and month.
    """

    df = get_customer_data()

    return customer_signup_yearwise_trend(df)


def average_cust_spend():

    df = get_customer_data()

    return get_avg_customer_spend(df)



def total_number_of_customers():

    df = get_customer_data()

    return get_total_customers(df)


def monthly_signup_counts():

    df = get_customer_data()

    return get_monthly_signup_counts(df)


def monthly_signup_by_gender():

    df = get_customer_data()

    return get_monthly_signup_by_gender(df)

def total_cust_by_gender():
    df = get_customer_data()
    return total_customers_by_gender(df)



# ============================================================
# TOOL REGISTRY
# ============================================================

CUSTOMER_TOOL_FUNCTIONS = {

    "total_number_of_customers":
        total_number_of_customers,

    "average_cust_spend":
        average_cust_spend,

    "monthly_signup_counts":
        monthly_signup_counts,

    "monthly_signup_by_gender":
        monthly_signup_by_gender,

    "customer_signup_year_wise_trend":
        customer_signup_year_wise_trend,

    "total_cust_by_gender":
        total_cust_by_gender,

}


# ============================================================
# OPENAI TOOL DEFINITIONS
# ============================================================

CUSTOMER_TOOLS = [

    {
        "type": "function",
        "name": "total_number_of_customers",
        "description": (
            "Get the total number of customers in the customer dataset."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "average_cust_spend",
        "description": (
            "Get the average amount spent by customers."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "monthly_signup_counts",
        "description": (
            "Get customer signup counts for each month."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "monthly_signup_by_gender",
        "description": (
            "Get customer signup counts by gender for each month."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "customer_signup_year_wise_trend",
        "description": (
            "Get customer signup trends broken down by year and month."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type":"function",
        "name":"total_cust_by_gender",
        "descritpion":(
            "Get gender wise customers in the customer data"
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        },
        "strict": True
    }
]