import os
from pathlib import Path
from fastapi import APIRouter, Request
from analytics.customer_analytics.data_loader import load_customer_data
from analytics.DemandForecasting.analysis import *

router = APIRouter(
    prefix="/api/demandforecasting",
    tags=["Demand Forecasting"]
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEMAND_FORECAST_FILEPATH = (
    BASE_DIR
    / "ML"
    / "DemandForecasting"
    / "results"
    / "2026_demand_forecast.csv"
)



df = load_customer_data(DEMAND_FORECAST_FILEPATH)

@router.get("/first_five_rows")
def first_five_rows():
    t = df.head(5)
    return t.to_dict(orient="records")

@router.get("/forecasted_kpis")
def forecasted_demand_units(
    from_date: str,
    to_date: str,
    product_name: str = None
):
    return get_forecast_kpis(
        df,
        from_date,
        to_date,
        product_name
    )

@router.get("/product_forecast")
def product_forecast(
    from_date: str,
    to_date: str,
    product_name: str
):
    return get_product_forecast(
        df,
        from_date,
        to_date,
        product_name
    )


@router.get("/top_products")
def top_products(
    from_date: str,
    to_date: str
):
    return get_top_products(
        df,
        from_date,
        to_date
    )
