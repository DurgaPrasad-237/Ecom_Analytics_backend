import os
from pathlib import Path
from fastapi import APIRouter, Request
from analytics.sales_analytics.analysis import *
from analytics.sales_analytics.data_loader import load_order_items_data
from analytics.sales_analytics.feature_engineering import fe

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRODUCTS_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "products_processed.csv"
)

ORDERS_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "orders_processed.csv"

)

ORDER_ITEMS_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "order_items_processed.csv"

)

p_df = load_order_items_data(PRODUCTS_FILEPATH)
oi_df = load_order_items_data(ORDER_ITEMS_FILEPATH)
orders = load_order_items_data(ORDERS_FILEPATH) # pive load anni common fiels so oka oka ratey chalu marchali
sales_df = oi_df.merge(
    p_df[['product_id', 'product_name', 'category']],
    on='product_id',
    how='left'
)
sales_df = sales_df.merge(
    orders[['order_id','order_date','order_time']],
    on="order_id",
    how="left"
)

sales_df = fe(sales_df)

router = APIRouter(
    prefix="/api/sales",
    tags=["Sales Analytics"]
)

@router.get("/sales-kpis")
def get_sales_kpis():
    print(sales_kpis(oi_df))
    return sales_kpis(oi_df)

@router.get("/top-profit-margin")
def get_top_profit_margin():

    result = product_profitability_analysis(sales_df)

    return (
        result
        .sort_values("profit_margin", ascending=False)
        .head(10)
        .to_dict(orient="records")
    )

@router.get("/top-revenue")
def get_top_revenue():

    result = product_profitability_analysis(sales_df)

    return (
        result
        .sort_values("revenue", ascending=False)
        .head(10)
        .to_dict(orient="records")
    )


@router.get("/top-profit")
def get_top_profit():

    result = product_profitability_analysis(sales_df)

    return (
        result
        .sort_values("profit", ascending=False)
        .head(10)
        .to_dict(orient="records")
    )


@router.get("/lowest-profit-margin")
def get_lowest_profit_margin():

    result = product_profitability_analysis(sales_df)

    return (
        result
        .sort_values("profit_margin", ascending=True)
        .head(10)
        .to_dict(orient="records")
    )


@router.get("/loss-making-order-rate")
def get_loss_making_order_rate():

    return (
        loss_making_order_rate(sales_df)
        .sort_values(
            "loss_making_order_rate",
            ascending=False
        )
        .head(10)
        .to_dict(orient="records")
    )

@router.get("/discount-vs-profit-margin")
def get_discount_vs_profit_margin():

    result = product_profitability_analysis(sales_df)

    return (
        result[
            [
                "product_name",
                "avg_discount",
                "profit_margin",
                "revenue",
                "profit"
            ]
        ]
        .sort_values("avg_discount", ascending=False)
        .to_dict(orient="records")
    )


@router.get("/monthly_profit_by_year")
def get_monthly_profit_by_year():
    return monthly_profit_by_year(sales_df)

@router.get("/monthly_revenue_by_year")
def get_monthly_revenue_by_year():
    return monthly_revenue_by_year(sales_df)