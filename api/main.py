import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from analytics.customer_analytics.data_loader import load_customer_data
from analytics.product_analytics.data_loader import load_fact_sales_data,load_productS_data,merge_product_fact_sales
from analytics.customer_analytics.analysis import (
    get_monthly_signup_by_gender,
    get_monthly_signup_counts,
    customer_signup_yearwise_trend,
    customer_churn_analysis,
    average_order_value_of_churned_customers,
    average_order_value_of_customer_status,
    customer_status_rate,
    customer_segment_analysis,
    get_total_customers,
    get_churn_rate,
    get_avg_customer_spend,
    get_avg_order_value,
)
from analytics.product_analytics.analysis import *

from ai.core.agent import Agent

load_dotenv()

app = FastAPI(
    title="Indian E-Commerce Analytics API",
    description="Backend API for e-commerce analytics",
    version="1.0.0",
)

origin = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

CUSTOMER_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "customers_processed.csv"
)

PRODUCTS_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "products_processed.csv"
)



df = load_customer_data(CUSTOMER_FILEPATH)
p_df = load_productS_data(PRODUCTS_FILEPATH)



# Create Agent once
agent = Agent(
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

product_agent = Agent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    domain="product"
)


@app.get("/")
def root():
    return {
        "message": "Indian E-Commerce Analytics API is running"
    }


# ---------------------------------------------------------
# CUSTOMER APIs
# ---------------------------------------------------------

@app.get("/api/customer/customer_segment")
def customer_segment():
    return customer_segment_analysis(df)


@app.get("/api/customer/avg_order_value")
def average_order_value():
    return get_avg_order_value(df)


@app.get("/api/customer/avg_cust_spend")
def average_customer_spend():
    return get_avg_customer_spend(df)


@app.get("/api/customer/churned_rate")
def churned_rate():
    return get_churn_rate(df)


@app.get("/api/customer/total_customers")
def total_customers():
    return get_total_customers(df)


@app.get("/api/customer/monthly-signups")
def monthly_signups():
    return get_monthly_signup_counts(df)


@app.get("/api/customer/monthly-signups-gender")
def monthly_signups_gender():
    return get_monthly_signup_by_gender(df)


@app.get("/api/customer/signup-trend")
def signup_trend():
    return customer_signup_yearwise_trend(df)


@app.get("/api/customer/churn")
def customer_churn():
    return customer_churn_analysis(df)


@app.get("/api/customer/status-rate")
def customer_status_rate_api():
    return customer_status_rate(df)


@app.get("/api/customer/segment-analysis")
def customer_segment_analysis_api():
    return customer_segment_analysis(df)


@app.get("/api/customer/churned-average-spend")
def churned_average_spend():
    return {
        "average_spend": average_order_value_of_churned_customers(df)
    }


@app.get("/api/customer/average-order-value-status")
def average_order_value_status():
    return average_order_value_of_customer_status(df)


# ----------------------------------------------------
# Products API
# ----------------------------------------------------

@app.get("/api/products/total_units_sold")
def total_units_sold():
    return total_number_of_unitsSold(p_df)

@app.get("/api/products/total_products")
def total_products():
    return total_number_of_products(p_df)


@app.get('/api/products/return_units')
def return_units():
    return total_returned_units(p_df)

@app.get('/api/products/avg_product_price')
def get_avg_product_price():
    return avg_product_price(p_df)

@app.get('/api/products/avg_product_cost')
def get_avg_product_cost():
    return avg_product_cost(p_df)

@app.get("/api/products/top_10_products_sold")
def get_top_10_products_sold():
    return top_10_products_sold(p_df)

@app.get("/api/products/top_10_rev_products")
def get_top_10_rev_products():
    return top_10_revenue_generate_products(p_df)


@app.get("/api/products/top_10_categories_sold")
def get_top_10_categories_sold():
    return top_10_which_category_sold(p_df)

@app.get("/api/products/price_vs_unitsSold")
def get_price_vs_units_sold():
    return price_vs_units_sold(p_df)


# @app.get("/api/products/top_10_revenue_products")
# def get_top_10_revenue_products():
#     return top_10_revenue_generate_products(m_fs_df)


# @app.get("/api/products/top_10_revenue_categories")
# def get_top_10_revenue_categories():
#     return top_10_revenue_generate_category(m_fs_df)


# @app.get("/api/products/top_profit_products")
# def get_top_profit_products():
#     return top_profit_products(m_fs_df)


# @app.get("/api/products/top_loss_products")
# def get_top_loss_products():
#     return top_loss_products(m_fs_df)


# @app.get("/api/products/top_return_rate_products")
# def get_top_return_rate_products():
#     return top_return_rate_products(m_fs_df)


# @app.get("/api/products/monthly_trend/{product_name}")
# def get_monthly_product_trend(product_name: str):
#     return monthly_trend_of_particular_product(m_fs_df, product_name)


# @app.get("/api/products/performance")
# def get_product_performance():
#     return product_performance(m_fs_df)



# ---------------------------------------------------------
# AI API
# ---------------------------------------------------------

@app.post("/api/ai/customer-chat")
async def customerChat(req: Request):

    data = await req.json()

    question = data["question"]
    chat_history = data.get("chat_history", [])

    result = agent.ask(
        question=question,
        chat_history=chat_history,
        provider="openai",
    )

    return result


@app.post("/api/ai/product-chat")
async def productChat(req: Request):

    data = await req.json()

    question = data["question"]
    chat_history = data.get("chat_history", [])

    print(question)
    print(chat_history)

    result = product_agent.ask(
        question=question,
        chat_history=chat_history,
        provider="openai",
    )

    return result