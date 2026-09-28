import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analytics.product_analytics.datahandling import handle_return_status
from analytics.product_analytics.datahandling import change_dates_datatype


def load_fact_sales_data(path):
    fact_sales = pd.read_csv(path)

    final_df = fact_sales [[
        'product_id',
        'quantity',
        'unit_price',
        'discount_percentage_item',
        'item_revenue',
        'item_cost',
        'profit',
        'order_date',
        'order_status',
        'delivery_state',
        'marketing_channel',
        'coupon_code',
        'refund_amount',
        'return_status',
        'rating',
        'review_sentiment',
        'expected_delivery_date',
        'actual_delivery_date',
        'delivery_days',
        'delivery_status',
        'delayed_flag'
    ]]

    final_df = handle_return_status(final_df)
    final_df = change_dates_datatype(final_df)


    return final_df


def load_productS_data(path):
    products = pd.read_csv(path)
    return products


def merge_product_fact_sales(final_df,products):
    final_df = final_df.merge(
        products[["product_id", "product_name","category","cost_price"]],
        on="product_id",
        how="left"
    )

    return final_df