import os
from pathlib import Path
from fastapi import APIRouter, Request
from analytics.customer_analytics.data_loader import load_customer_data
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


router = APIRouter(
    prefix="/api/customer",
    tags=["Customer Analytics"]
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CUSTOMER_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "customers_processed.csv"
)


df = load_customer_data(CUSTOMER_FILEPATH)



@router.get("/customer_segment")
def customer_segment():
    return customer_segment_analysis(df)


@router.get("/avg_order_value")
def average_order_value():
    return get_avg_order_value(df)


@router.get("/avg_cust_spend")
def average_customer_spend():
    return get_avg_customer_spend(df)


@router.get("/churned_rate")
def churned_rate():
    return get_churn_rate(df)


@router.get("/total_customers")
def total_customers():
    return get_total_customers(df)


@router.get("/monthly-signups")
def monthly_signups():
    return get_monthly_signup_counts(df)


@router.get("/monthly-signups-gender")
def monthly_signups_gender():
    return get_monthly_signup_by_gender(df)


@router.get("/signup-trend")
def signup_trend():
    return customer_signup_yearwise_trend(df)


@router.get("/churn")
def customer_churn():
    return customer_churn_analysis(df)


@router.get("/status-rate")
def customer_status_rate_api():
    return customer_status_rate(df)


@router.get("/segment-analysis")
def customer_segment_analysis_api():
    return customer_segment_analysis(df)


@router.get("/churned-average-spend")
def churned_average_spend():
    return {
        "average_spend": average_order_value_of_churned_customers(df)
    }


@router.get("/average-order-value-status")
def average_order_value_status():
    return average_order_value_of_customer_status(df)


