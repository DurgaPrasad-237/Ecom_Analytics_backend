import pandas as pd
 




def load_products(df:pd.DataFrame):
    product_names = (
        df["product_name"]
        .dropna()
        .unique()
        .tolist()
    )

    return product_names


def get_inventory_demand_by_product(df:pd.DataFrame,product_name:str) -> dict:
    result = df.loc[df['product_name'] == product_name,:]
    return result.to_dict(orient="records")



import pandas as pd


def get_inventory_position(
    df: pd.DataFrame,
    forecast_df: pd.DataFrame,
    product_name: str,
    lead_time_days: int = 7
) -> list:

    # ---------------------------------------------
    # Get current stock
    # ---------------------------------------------

    product_inventory = df.loc[
        df["product_name"] == product_name
    ]

    if product_inventory.empty:
        return []

    current_stock = product_inventory.iloc[0]["stock_quantity"]

    # ---------------------------------------------
    # Get forecast for selected product
    # ---------------------------------------------

    product_forecast = forecast_df.loc[
        forecast_df["product_name"] == product_name
    ].copy()

    if product_forecast.empty:
        return []

    # Convert date
    product_forecast["forecast_date"] = pd.to_datetime(
        product_forecast["forecast_date"]
    )

    # Sort by date
    product_forecast = product_forecast.sort_values(
        "forecast_date"
    )

    # ---------------------------------------------
    # First forecast date
    # ---------------------------------------------

    start_date = product_forecast[
        "forecast_date"
    ].min()

    # ---------------------------------------------
    # Get forecast during lead time
    # ---------------------------------------------

    lead_time_forecast = product_forecast.loc[
        (
            product_forecast["forecast_date"]
            >= start_date
        )
        &
        (
            product_forecast["forecast_date"]
            < start_date
            + pd.Timedelta(days=lead_time_days)
        )
    ].copy()

    # ---------------------------------------------
    # Calculate inventory position
    # ---------------------------------------------

    lead_time_forecast[
        "cumulative_demand"
    ] = (
        lead_time_forecast[
            "forecast_demand"
        ].cumsum()
    )

    lead_time_forecast[
        "expected_inventory"
    ] = (
        current_stock
        - lead_time_forecast[
            "cumulative_demand"
        ]
    ).clip(lower=0)

    # ---------------------------------------------
    # Add Today row
    # ---------------------------------------------

    today_row = pd.DataFrame({
        "forecast_date": [start_date],
        "forecast_demand": [0],
        "cumulative_demand": [0],
        "expected_inventory": [current_stock]
    })

    lead_time_forecast = pd.concat(
        [
            today_row,
            lead_time_forecast
        ],
        ignore_index=True
    )

    # ---------------------------------------------
    # Remove duplicate first date
    # ---------------------------------------------

    lead_time_forecast = (
        lead_time_forecast
        .drop_duplicates(
            subset="forecast_date",
            keep="first"
        )
        .reset_index(drop=True)
    )

    # ---------------------------------------------
    # Day labels
    # ---------------------------------------------

    lead_time_forecast["day"] = [
        "Today"
    ] + [
        f"Day {i}"
        for i in range(
            1,
            len(lead_time_forecast)
        )
    ]

    # ---------------------------------------------
    # Return API-friendly data
    # ---------------------------------------------

    result = lead_time_forecast[
        [
            "forecast_date",
            "day",
            "forecast_demand",
            "expected_inventory"
        ]
    ].copy()

    # Convert date to string for JSON
    result["forecast_date"] = (
        result["forecast_date"]
        .dt.strftime("%Y-%m-%d")
    )

    # Convert numeric values
    result["forecast_demand"] = (
        result["forecast_demand"]
        .round(2)
    )

    result["expected_inventory"] = (
        result["expected_inventory"]
        .round(2)
    )

    return result.to_dict(
        orient="records"
    )


import pandas as pd
import math


def get_inventory_products(
    df: pd.DataFrame,
    page: int = 1,
    page_size: int = 10,
    stock_filter: str = "all",
    search: str = ""
) -> dict:

    result = df.copy()

    # --------------------------------------------------
    # Create stock status
    # --------------------------------------------------

    result["stock_status"] = "Healthy"

    # Critical:
    # Current stock is less than lead-time demand
    critical_mask = (
        result["stock_quantity"]
        < result["lead_time_demand"]
    )

    result.loc[
        critical_mask,
        "stock_status"
    ] = "Critical"

    # Reorder Required:
    # Current stock is below reorder point
    # but not below lead-time demand
    reorder_mask = (
        (result["stock_quantity"] < result["reorder_point"])
        & (~critical_mask)
    )

    result.loc[
        reorder_mask,
        "stock_status"
    ] = "Reorder Required"

    # --------------------------------------------------
    # Search by product name
    # --------------------------------------------------

    if search:
        result = result.loc[
            result["product_name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # --------------------------------------------------
    # Stock status filter
    # --------------------------------------------------

    if stock_filter == "healthy":

        result = result.loc[
            result["stock_status"] == "Healthy"
        ]

    elif stock_filter == "reorder":

        result = result.loc[
            result["stock_status"] == "Reorder Required"
        ]

    elif stock_filter == "critical":

        result = result.loc[
            result["stock_status"] == "Critical"
        ]

    # --------------------------------------------------
    # Total records after filtering
    # --------------------------------------------------

    total_products = len(result)

    # --------------------------------------------------
    # Pagination validation
    # --------------------------------------------------

    page = max(page, 1)
    page_size = max(page_size, 1)

    total_pages = math.ceil(
        total_products / page_size
    )

    # If requested page is beyond available pages
    if total_pages > 0 and page > total_pages:
        page = total_pages

    # --------------------------------------------------
    # Pagination
    # --------------------------------------------------

    start = (page - 1) * page_size
    end = start + page_size

    paginated_result = result.iloc[
        start:end
    ].copy()

    # --------------------------------------------------
    # Select columns
    # --------------------------------------------------

    paginated_result = paginated_result[
        [
            "product_name",
            "total_forecast_demand",
            "average_daily_demand",
            "maximum_daily_demand",
            "lead_time_demand",
            "safety_stock",
            "reorder_point",
            "recommended_inventory",
            "stock_quantity",
            "stock_status"
        ]
    ]

    # --------------------------------------------------
    # Round numeric values
    # --------------------------------------------------

    numeric_columns = [
        "total_forecast_demand",
        "average_daily_demand",
        "maximum_daily_demand",
        "lead_time_demand",
        "safety_stock",
        "reorder_point",
        "recommended_inventory"
    ]

    paginated_result[numeric_columns] = (
        paginated_result[numeric_columns]
        .round(2)
    )

    # --------------------------------------------------
    # Return API response
    # --------------------------------------------------

    return {
        "data": paginated_result.to_dict(
            orient="records"
        ),
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_products": total_products,
            "total_pages": total_pages
        }
    }