import requests

BASE_URL = "http://127.0.0.1:8000"

def get_customer_segment():
    response = requests.get(
        f"{BASE_URL}/api/customer/customer_segment"
    )
    response.raise_for_status()
    return response.json()

def get_avg_order_value():
    response = requests.get(
        f"{BASE_URL}/api/customer/avg_order_value"
    )
    response.raise_for_status()
    return response.json()


def get_avg_customer_spend():
    response = requests.get(
        f"{BASE_URL}/api/customer/avg_cust_spend"
    )
    response.raise_for_status()
    return response.json()

def get_churned_rate():
    response = requests.get(
        f"{BASE_URL}/api/customer/churned_rate"
    )
    response.raise_for_status()
    return response.json()

def get_total_customers():
    response = requests.get(
        f"{BASE_URL}/api/customer/total_customers"
    )
  
    response.raise_for_status()
    
    return response.json()

def get_monthly_signups():
    response = requests.get(
        f"{BASE_URL}/api/customer/monthly-signups"
    )
    
    response.raise_for_status()
    return response.json()


def get_monthly_signups_gender():
    response = requests.get(
        f"{BASE_URL}/api/customer/monthly-signups-gender"
    )
    response.raise_for_status()
    return response.json()


def get_signup_trend():
    response = requests.get(
        f"{BASE_URL}/api/customer/signup-trend"
    )
    response.raise_for_status()
    return response.json()


def get_customer_churn():
    response = requests.get(
        f"{BASE_URL}/api/customer/churn"
    )
   
    response.raise_for_status()
    return response.json()


def get_status_rate():
    response = requests.get(
        f"{BASE_URL}/api/customer/status-rate"
    )
    response.raise_for_status()
    return response.json()


def get_segment_analysis():
    response = requests.get(
        f"{BASE_URL}/api/customer/segment-analysis"
    )
    response.raise_for_status()
    return response.json()



# -----------------------------------------
def get_total_units_sold():
    response = requests.get(
        f"{BASE_URL}/api/products/total_units_sold"
    )
    response.raise_for_status()
    return response.json()


def get_total_revenue():
    response = requests.get(
        f"{BASE_URL}/api/products/total_revenue"
    )
    response.raise_for_status()
    return response.json()


def get_total_profit():
    response = requests.get(
        f"{BASE_URL}/api/products/total_profit"
    )
    response.raise_for_status()
    return response.json()


def get_total_product_cost():
    response = requests.get(
        f"{BASE_URL}/api/products/total_pro_cost"
    )
    response.raise_for_status()
    return response.json()


def get_profit_margin():
    response = requests.get(
        f"{BASE_URL}/api/products/profit_margin"
    )
    response.raise_for_status()
    return response.json()


def get_total_returns():
    response = requests.get(
        f"{BASE_URL}/api/products/total_returns"
    )
    response.raise_for_status()
    return response.json()


def get_product_return_rate():
    response = requests.get(
        f"{BASE_URL}/api/products/return_rate"
    )
    response.raise_for_status()
    return response.json()


def get_top_10_products_sold():
    response = requests.get(
        f"{BASE_URL}/api/products/top_10_products_sold"
    )
    response.raise_for_status()
    return response.json()


def get_top_10_categories_sold():
    response = requests.get(
        f"{BASE_URL}/api/products/top_10_categories_sold"
    )
    response.raise_for_status()
    return response.json()


def get_top_10_revenue_products():
    response = requests.get(
        f"{BASE_URL}/api/products/top_10_revenue_products"
    )
    response.raise_for_status()
    return response.json()


def get_top_10_revenue_categories():
    response = requests.get(
        f"{BASE_URL}/api/products/top_10_revenue_categories"
    )
    response.raise_for_status()
    return response.json()


def get_top_profit_products():
    response = requests.get(
        f"{BASE_URL}/api/products/top_profit_products"
    )
    response.raise_for_status()
    return response.json()


def get_top_loss_products():
    response = requests.get(
        f"{BASE_URL}/api/products/top_loss_products"
    )
    response.raise_for_status()
    return response.json()


def get_top_return_rate_products():
    response = requests.get(
        f"{BASE_URL}/api/products/top_return_rate_products"
    )
    response.raise_for_status()
    return response.json()


def get_monthly_product_trend(product_name):
    response = requests.get(
        f"{BASE_URL}/api/products/monthly_trend/{product_name}"
    )
    response.raise_for_status()
    return response.json()


def get_product_performance():
    response = requests.get(
        f"{BASE_URL}/api/products/performance"
    )
    response.raise_for_status()
    return response.json()