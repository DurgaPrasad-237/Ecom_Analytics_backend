import os
from pathlib import Path
from fastapi import APIRouter, Request
from analytics.product_analytics.analysis import *
from analytics.product_analytics.data_loader import load_productS_data


BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRODUCTS_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "products_processed.csv"
)

p_df = load_productS_data(PRODUCTS_FILEPATH)


router = APIRouter(
    prefix="/api/products",
    tags=["Products Analytics"]
)

@router.get("/total_units_sold")
def total_units_sold():
    return total_number_of_unitsSold(p_df)

@router.get("/total_products")
def total_products():
    return total_number_of_products(p_df)


@router.get('/return_units')
def return_units():
    return total_returned_units(p_df)

@router.get('/avg_product_price')
def get_avg_product_price():
    return avg_product_price(p_df)

@router.get('/avg_product_cost')
def get_avg_product_cost():
    return avg_product_cost(p_df)

@router.get("/top_10_products_sold")
def get_top_10_products_sold():
    return top_10_products_sold(p_df)

@router.get("/top_10_rev_products")
def get_top_10_rev_products():
    return top_10_revenue_generate_products(p_df)


@router.get("/top_10_categories_sold")
def get_top_10_categories_sold():
    return top_10_which_category_sold(p_df)

@router.get("/price_vs_unitsSold")
def get_price_vs_units_sold():
    return price_vs_units_sold(p_df)


