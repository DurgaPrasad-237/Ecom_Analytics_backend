import time
from pathlib import Path

import dagshub
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import ElasticNet
from sklearn.pipeline import Pipeline

from ML.DemandForecasting.feature_engineering import (
    periods,
    lag_features,
    rolling_features
)


# ============================================================
# DagsHub / MLflow
# ============================================================

dagshub.init(
    repo_owner="DurgaPrasad-237",
    repo_name="Ecom_Analytics_backend",
    mlflow=True
)

mlflow.set_experiment("Demand Forecasting")


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "processed"

MODEL_DIR = (
    BASE_DIR
    / "ML"
    / "DemandForecasting"
    / "models"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD DATA
# ============================================================

orders = pd.read_csv(
    DATA_DIR / "ORDERS_processed.csv"
)

order_items = pd.read_csv(
    DATA_DIR / "order_items_processed.csv"
)

products = pd.read_csv(
    DATA_DIR / "products_processed.csv"
)


# ============================================================
# DATE
# ============================================================

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)


# ============================================================
# MERGE ORDER ITEMS + PRODUCTS
# ============================================================

df = order_items.merge(
    products[
        [
            "product_id",
            "product_name"
        ]
    ],
    on="product_id",
    how="left"
)


# ============================================================
# MERGE WITH ORDERS
# ============================================================

df = df.merge(
    orders[
        [
            "order_id",
            "order_date"
        ]
    ],
    on="order_id",
    how="inner"
)


print("Merged data shape:", df.shape)


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "product_name",
    "order_date",
    "quantity"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ============================================================
# DAILY DEMAND
# ============================================================

daily_demand = (
    df.groupby(
        [
            "product_name",
            "order_date"
        ],
        as_index=False
    )["quantity"]
    .sum()
)


# ============================================================
# CREATE COMPLETE PRODUCT-DATE GRID
# ============================================================

products_list = (
    daily_demand["product_name"]
    .dropna()
    .unique()
)

date_range = pd.date_range(
    start=daily_demand["order_date"].min(),
    end=daily_demand["order_date"].max(),
    freq="D"
)

complete_index = pd.MultiIndex.from_product(
    [
        products_list,
        date_range
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


print(
    "Daily demand shape:",
    daily_demand.shape
)


# ============================================================
# FEATURE ENGINEERING
# ============================================================

daily_demand = periods(
    daily_demand
)

daily_demand = lag_features(
    daily_demand
)

daily_demand = rolling_features(
    daily_demand
)


# ============================================================
# REMOVE ROWS WITHOUT ENOUGH HISTORY
# ============================================================

daily_demand = daily_demand.dropna(
    subset=[
        "lag_28",
        "rolling_mean_28"
    ]
).reset_index(drop=True)


# ============================================================
# USE ONLY 2023–2025
# ============================================================

daily_demand = daily_demand[
    daily_demand["order_date"].dt.year <= 2025
].copy()


print(
    "Final training date range:",
    daily_demand["order_date"].min(),
    "to",
    daily_demand["order_date"].max()
)

print(
    "Final training rows:",
    len(daily_demand)
)


# ============================================================
# FEATURES
# ============================================================

target = "quantity"

categorical_features = [
    "product_name"
]

numeric_features = [
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


X = daily_demand[
    categorical_features
    + numeric_features
]

y = daily_demand[target]


# ============================================================
# PREPROCESSOR
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numeric",
            StandardScaler(),
            numeric_features
        )
    ]
)


# ============================================================
# FINAL ELASTICNET
# ============================================================

model = ElasticNet(
    alpha=0.01,
    l1_ratio=0.9,
    max_iter=10000
)


pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)


# ============================================================
# FINAL TRAINING
# ============================================================

print("\nStarting final ElasticNet training...")

start_time = time.time()


with mlflow.start_run(
    run_name="final_elasticnet_2023_2025"
):

    pipeline.fit(
        X,
        y
    )

    training_time = (
        time.time()
        - start_time
    )


    # ========================================================
    # LOG PARAMETERS
    # ========================================================

    mlflow.log_params(
        {
            "model": "elasticnet_tuned",
            "alpha": 0.01,
            "l1_ratio": 0.9,
            "max_iter": 10000,
            "training_period": "2023-2025"
        }
    )


    # ========================================================
    # LOG TAGS
    # ========================================================

    mlflow.set_tag(
        "stage",
        "final_training"
    )

    mlflow.set_tag(
        "model_status",
        "final"
    )

    mlflow.set_tag(
        "dataset_period",
        "2023-2025"
    )


    # ========================================================
    # LOG METRICS
    # ========================================================

    mlflow.log_metrics(
        {
            "training_time_seconds":
                training_time,

            "training_rows":
                len(X)
        }
    )


    # ========================================================
    # SAVE FINAL MODEL
    # ========================================================

    model_file = (
        MODEL_DIR
        / "final_demand_forecasting_elasticnet.pkl"
    )


    joblib.dump(
        pipeline,
        model_file
    )


    # ========================================================
    # LOG PICKLE ARTIFACT
    # ========================================================

    mlflow.log_artifact(
        str(model_file)
    )


    # ========================================================
    # LOG MODEL TO MLflow
    # ========================================================

    mlflow.sklearn.log_model(
        sk_model=pipeline,
        name="final_elasticnet_model"
    )


    # ========================================================
    # PRINT RESULTS
    # ========================================================

    print(
        "\nFinal model trained successfully."
    )

    print(
        "Model:",
        model_file
    )

    print(
        "Training rows:",
        len(X)
    )

    print(
        "Training time:",
        round(
            training_time,
            2
        ),
        "seconds"
    )

    print(
        "Alpha:",
        0.01
    )

    print(
        "L1 ratio:",
        0.9
    )

    print(
        "\nMLflow run completed."
    )