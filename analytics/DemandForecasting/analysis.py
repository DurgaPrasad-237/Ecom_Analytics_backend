import pandas as pd
import numpy as np

def get_forecast_kpis(
    df: pd.DataFrame,
    from_date: str,
    to_date: str,
    product_name: str = None
) -> dict:

    filter_df = df.loc[
        (df['forecast_date'] >= from_date) &
        (df['forecast_date'] <= to_date),
        :
    ]

    # Filter by product only when a specific product is selected
    if product_name:
        filter_df = filter_df.loc[
            filter_df['product_name'] == product_name
        ]

    forecast_demand = filter_df['forecast_demand'].sum()

    daily_demand = (
        filter_df
        .groupby('forecast_date')['forecast_demand']
        .sum()
    )

    average_daily_demand = daily_demand.mean()
    peak_demand = daily_demand.max()

    return {
        "forecasted_demand": int(forecast_demand),
        "average_daily_demand": average_daily_demand,
        "peak_daily_demand": peak_demand
    }  



def get_product_forecast(
    df: pd.DataFrame,
    from_date: str,
    to_date: str,
    product_name: str
) -> list:

    filter_df = df.loc[
        (df['forecast_date'] >= from_date) &
        (df['forecast_date'] <= to_date) &
        (df['product_name'] == product_name)
    ]

    daily_demand = (
        filter_df
        .groupby('forecast_date')['forecast_demand']
        .sum()
        .reset_index()
    )

    return [
        {
            "date": row["forecast_date"],
            "demand": round(row["forecast_demand"], 2)
        }
        for _, row in daily_demand.iterrows()
    ]


def get_top_products(
    df: pd.DataFrame,
    from_date: str,
    to_date: str
) -> list:

    filter_df = df.loc[
        (df['forecast_date'] >= from_date) &
        (df['forecast_date'] <= to_date)
    ]

    top_products = (
        filter_df
        .groupby('product_name')['forecast_demand']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    return [
        {
            "product_name": row["product_name"],
            "forecast_demand": round(row["forecast_demand"], 2)
        }
        for _, row in top_products.iterrows()
    ]