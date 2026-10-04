# ML/DemandForecasting/forecast.py

import pandas as pd
import mlflow
import dagshub

from pathlib import Path

from ML.DemandForecasting.feature_engineering import (
    periods,
    lag_features,
    rolling_features
)


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ORDERS_FILE = BASE_DIR / "data" / "processed" / "ORDERS_processed.csv"
ORDER_ITEMS_FILE = BASE_DIR / "data" / "processed" / "order_items_processed.csv"
PRODUCTS_FILE = BASE_DIR / "data" / "processed" / "products_processed.csv"

RESULTS_DIR = BASE_DIR / "ML" / "DemandForecasting" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. DAGSHUB / MLFLOW
# ============================================================

dagshub.init(
    repo_owner="DurgaPrasad-237",
    repo_name="Ecom_Analytics_backend",
    mlflow=True
)

mlflow.set_experiment("Demand Forecasting")


# ============================================================
# 3. LOAD REGISTERED MODEL
# ============================================================

MODEL_URI = "models:/DemandForecastingModel@production"

print("Loading registered model...")

model = mlflow.pyfunc.load_model(MODEL_URI)

print("Registered model loaded successfully.")


# ============================================================
# 4. LOAD DATA
# ============================================================

orders = pd.read_csv(ORDERS_FILE)
order_items = pd.read_csv(ORDER_ITEMS_FILE)
products = pd.read_csv(PRODUCTS_FILE)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)


# ============================================================
# 5. MERGE DATA
# ============================================================

order_items = order_items.merge(
    products[
        [
            "product_id",
            "product_name"
        ]
    ],
    on="product_id",
    how="left"
)

data = order_items.merge(
    orders[
        [
            "order_id",
            "order_date"
        ]
    ],
    on="order_id",
    how="left"
)


# ============================================================
# 6. DAILY DEMAND
# ============================================================

daily_demand = (
    data
    .groupby(
        [
            "product_name",
            "order_date"
        ],
        as_index=False
    )["quantity"]
    .sum()
)


# ============================================================
# 7. COMPLETE PRODUCT-DATE GRID
# ============================================================

all_products = (
    daily_demand["product_name"]
    .dropna()
    .unique()
)

all_dates = pd.date_range(
    start=daily_demand["order_date"].min(),
    end=daily_demand["order_date"].max(),
    freq="D"
)

complete_index = pd.MultiIndex.from_product(
    [
        all_products,
        all_dates
    ],
    names=[
        "product_name",
        "order_date"
    ]
)

daily_demand = (
    daily_demand
    .set_index(
        [
            "product_name",
            "order_date"
        ]
    )
    .reindex(
        complete_index,
        fill_value=0
    )
    .reset_index()
)


# ============================================================
# 8. FEATURE ENGINEERING
# ============================================================

daily_demand = periods(daily_demand)

daily_demand = lag_features(daily_demand)

daily_demand = rolling_features(daily_demand)

daily_demand = daily_demand.dropna(
    subset=[
        "lag_28",
        "rolling_mean_28"
    ]
).reset_index(drop=True)


# ============================================================
# 9. PREPARE HISTORY
# ============================================================

history = daily_demand[
    [
        "product_name",
        "order_date",
        "quantity"
    ]
].copy()

history = history.rename(
    columns={
        "quantity": "demand"
    }
)

history = history.sort_values(
    [
        "product_name",
        "order_date"
    ]
).reset_index(drop=True)


# ============================================================
# 10. CREATE FAST LOOKUP STRUCTURE
# ============================================================
#
# Instead of repeatedly doing:
#
# history[history["product_name"] == product]
#
# we create one dictionary per product.
#
# Each product stores only its demand history.
#

product_history = {}

for product, group in history.groupby("product_name"):

    product_history[product] = (
        group["demand"]
        .astype(float)
        .tolist()
    )


# ============================================================
# 11. PRODUCTS AND DATES
# ============================================================

products_list = list(
    product_history.keys()
)

latest_actual_date = data["order_date"].max()

forecast_start = latest_actual_date + pd.Timedelta(days=1)

future_dates = pd.date_range(
    start=forecast_start,
    end="2026-12-31",
    freq="D"
)

print()
print("Preparing 2026 forecast...")
print(
    f"Products: {len(products_list)}"
)
print(
    f"Forecast days: {len(future_dates)}"
)


# ============================================================
# 12. MODEL FEATURES
# ============================================================

feature_columns = [
    "product_name",
    "year",
    "month",
    "day_of_week",
    "week_of_year",
    "quarter",
    "lag_1",
    "lag_7",
    "lag_14",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_14",
    "rolling_mean_28"
]

numeric_float_features = [
    "lag_1",
    "lag_7",
    "lag_14",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_14",
    "rolling_mean_28"
]


# ============================================================
# 13. RECURSIVE FORECASTING
# ============================================================

predictions = []

total_days = len(future_dates)

for day_number, current_date in enumerate(
    future_dates,
    start=1
):

    rows = []

    # --------------------------------------------------------
    # Build features for ALL products
    # --------------------------------------------------------

    for product in products_list:

        demand_values = product_history[product]

        # Need 28 observations
        if len(demand_values) < 28:
            continue

        row = {
            "product_name": product,

            "year": int(current_date.year),

            "month": int(current_date.month),

            "day_of_week": int(
                current_date.dayofweek
            ),

            "week_of_year": int(
                current_date.isocalendar().week
            ),

            "quarter": int(
                current_date.quarter
            ),

            "lag_1": float(
                demand_values[-1]
            ),

            "lag_7": float(
                demand_values[-7]
            ),

            "lag_14": float(
                demand_values[-14]
            ),

            "lag_28": float(
                demand_values[-28]
            ),

            "rolling_mean_7": float(
                sum(
                    demand_values[-7:]
                ) / 7
            ),

            "rolling_mean_14": float(
                sum(
                    demand_values[-14:]
                ) / 14
            ),

            "rolling_mean_28": float(
                sum(
                    demand_values[-28:]
                ) / 28
            )
        }

        rows.append(row)


    # --------------------------------------------------------
    # Create prediction dataframe
    # --------------------------------------------------------

    X_future = pd.DataFrame(rows)

    if X_future.empty:
        continue

    X_future = X_future[
        feature_columns
    ]


    # ========================================================
    # MATCH MLFLOW MODEL SIGNATURE
    # ========================================================

    X_future[
        numeric_float_features
    ] = X_future[
        numeric_float_features
    ].astype("float64")

    X_future[
        [
            "year",
            "month",
            "day_of_week",
            "week_of_year",
            "quarter"
        ]
    ] = X_future[
        [
            "year",
            "month",
            "day_of_week",
            "week_of_year",
            "quarter"
        ]
    ].astype("int64")


    # ========================================================
    # PREDICT ALL PRODUCTS AT ONCE
    # ========================================================

    predictions_current = model.predict(
        X_future
    )


    # --------------------------------------------------------
    # Convert prediction output
    # --------------------------------------------------------

    if isinstance(
        predictions_current,
        pd.DataFrame
    ):
        predictions_current = (
            predictions_current.iloc[:, 0]
        )

    elif not isinstance(
        predictions_current,
        pd.Series
    ):
        predictions_current = pd.Series(
            predictions_current
        )

    predictions_current = (
        predictions_current
        .astype(float)
        .clip(lower=0)
        .reset_index(drop=True)
    )


    # ========================================================
    # SAVE PREDICTIONS + UPDATE HISTORY
    # ========================================================

    for i, product in enumerate(
        X_future["product_name"]
    ):

        predicted_demand = float(
            predictions_current.iloc[i]
        )

        predictions.append(
            {
                "product_name": product,

                "forecast_date": current_date,

                "forecast_demand": predicted_demand
            }
        )

        # IMPORTANT:
        # Add today's prediction to the product's
        # history for tomorrow's lag/rolling features.

        product_history[product].append(
            predicted_demand
        )


    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    if (
        day_number == 1
        or day_number % 30 == 0
        or day_number == total_days
    ):

        print(
            f"Progress: "
            f"{day_number}/{total_days} days "
            f"({day_number / total_days * 100:.1f}%)"
        )


# ============================================================
# 14. FINAL FORECAST DATAFRAME
# ============================================================

forecast_result = pd.DataFrame(
    predictions
)


# ============================================================
# 15. SAVE FORECAST
# ============================================================

forecast_file = (
    RESULTS_DIR /
    "2026_demand_forecast.csv"
)

forecast_result.to_csv(
    forecast_file,
    index=False
)


# ============================================================
# 16. SUMMARY
# ============================================================

print()
print("=" * 60)
print("2026 DEMAND FORECAST COMPLETED")
print("=" * 60)

print(
    f"Forecast rows       : "
    f"{len(forecast_result):,}"
)

print(
    f"Products            : "
    f"{forecast_result['product_name'].nunique():,}"
)

print(
    f"Forecast days       : "
    f"{forecast_result['forecast_date'].nunique():,}"
)

print(
    f"Total forecast demand: "
    f"{forecast_result['forecast_demand'].sum():,.2f}"
)

print(
    f"Saved to            : "
    f"{forecast_file}"
)

print("=" * 60)

print()
print("Sample forecast:")

print(
    forecast_result.head(10)
)