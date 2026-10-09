import os
from pathlib import Path
from fastapi import APIRouter, Request
from analytics.customer_analytics.data_loader import load_customer_data
from analytics.InventoryPlanning.analysis import *


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

router = APIRouter(
    prefix="/api/inventoryplanning",
    tags=["Inventory Planning"]
)


@router.get("/get-products")
def get_products():
    return load_products(final_df)


@router.get("/get-inventory-demand-by-product")
def inventory_demand_by_products(product_name:str):
    return get_inventory_demand_by_product(final_df,product_name)


@router.get("/inventory-position")
def inventory_position(
    product_name: str
):
    return get_inventory_position(
        final_df,
        forecast_df,
        product_name
    )

@router.get("/inventory-products")
def inventory_products(
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