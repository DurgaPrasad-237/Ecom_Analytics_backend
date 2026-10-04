import joblib
import mlflow
import dagshub

import numpy as np
import pandas as pd

from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from ML.DemandForecasting.feature_engineering import (
    periods,
    lag_features,
    rolling_features
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ORDERS_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "ORDERS_processed.csv"
)

PRODUCTS_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "products_processed.csv"
)

ORDER_ITEMS_FILEPATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "order_items_processed.csv"
)

MODEL_DIR = (
    BASE_DIR
    / "ML"
    / "DemandForecasting"
    / "models"
)

RESULTS_DIR = (
    BASE_DIR
    / "ML"
    / "DemandForecasting"
    / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# DATA LOADING
# ============================================================

def load_data(file_path):

    return pd.read_csv(file_path)


# ============================================================
# MERGE DATA
# ============================================================

def merge_dataframes(
    first_df,
    second_df,
    on
):

    return first_df.merge(
        second_df,
        on=on,
        how="left"
    )


# ============================================================
# CREATE DAILY DEMAND
# ============================================================

def create_daily_demand_dataframe(df):

    daily_demand = (
        df
        .groupby(
            ["product_name", "order_date"]
        )["quantity"]
        .sum()
        .reset_index()
    )

    daily_demand["order_date"] = pd.to_datetime(
        daily_demand["order_date"]
    )

    daily_demand = daily_demand.sort_values(
        ["product_name", "order_date"]
    )

    # Continuous daily demand
    daily_demand = (
        daily_demand
        .set_index("order_date")
        .groupby("product_name")["quantity"]
        .resample("D")
        .sum()
        .reset_index()
    )

    daily_demand = daily_demand.sort_values(
        ["product_name", "order_date"]
    )

    # Calendar features
    daily_demand = periods(
        daily_demand
    )

    # Lag features
    daily_demand = lag_features(
        daily_demand
    )

    # Rolling features
    daily_demand = rolling_features(
        daily_demand
    )

    # Remove rows without enough history
    daily_demand = daily_demand.dropna(
        subset=[
            "lag_28",
            "rolling_mean_28"
        ]
    ).reset_index(drop=True)

    return daily_demand


# ============================================================
# GET 2025 TEST DATA
# ============================================================

def get_test_data(daily_demand):

    test = daily_demand[
        daily_demand["year"] == 2025
    ].copy()

    X_test = test.drop(
        columns=[
            "quantity",
            "order_date"
        ]
    )

    y_test = test["quantity"]

    return X_test, y_test


# ============================================================
# WAPE
# ============================================================

def calculate_wape(
    y_true,
    y_pred
):

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    denominator = np.sum(
        np.abs(y_true)
    )

    if denominator == 0:
        return np.nan

    numerator = np.sum(
        np.abs(
            y_true - y_pred
        )
    )

    return (
        numerator
        / denominator
        * 100
    )


# ============================================================
# CALCULATE METRICS
# ============================================================

def calculate_metrics(
    y_true,
    y_pred
):

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )

    r2 = r2_score(
        y_true,
        y_pred
    )

    wape = calculate_wape(
        y_true,
        y_pred
    )

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "wape": wape
    }


# ============================================================
# GET ALL MODELS
# ============================================================

def get_model_files():

    model_files = sorted(
        MODEL_DIR.glob("*.pkl")
    )

    return model_files


# ============================================================
# EVALUATE MODELS
# ============================================================

def evaluate_models(
    model_files,
    X_test,
    y_test
):

    results = []

    for model_file in model_files:

        model_name = model_file.stem

        print(
            "\n========================================"
        )

        print(
            f"Evaluating: {model_name}"
        )

        print(
            "========================================"
        )

        # ----------------------------------------------------
        # Load model
        # ----------------------------------------------------

        model = joblib.load(
            model_file
        )

        # ----------------------------------------------------
        # Predict
        # ----------------------------------------------------

        y_pred = model.predict(
            X_test
        )

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------

        metrics = calculate_metrics(
            y_test,
            y_pred
        )

        mae = metrics["mae"]
        rmse = metrics["rmse"]
        r2 = metrics["r2"]
        wape = metrics["wape"]

        # ----------------------------------------------------
        # MLflow run
        # ----------------------------------------------------

        with mlflow.start_run(
            run_name=f"evaluation_{model_name}"
        ):

            mlflow.log_param(
                "model",
                model_name
            )

            mlflow.log_param(
                "evaluation_year",
                2025
            )

            mlflow.log_param(
                "dataset",
                "2025_test"
            )

            mlflow.log_metric(
                "mae",
                mae
            )

            mlflow.log_metric(
                "rmse",
                rmse
            )

            mlflow.log_metric(
                "r2",
                r2
            )

            mlflow.log_metric(
                "wape",
                wape
            )

            mlflow.set_tag(
                "stage",
                "evaluation"
            )

            mlflow.set_tag(
                "selection_status",
                "candidate"
            )

        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        results.append(
            {
                "model": model_name,
                "mae": mae,
                "rmse": rmse,
                "r2": r2,
                "wape": wape
            }
        )

        print(
            f"MAE  : {mae:.4f}"
        )

        print(
            f"RMSE : {rmse:.4f}"
        )

        print(
            f"R²   : {r2:.4f}"
        )

        print(
            f"WAPE : {wape:.2f}%"
        )

    return pd.DataFrame(
        results
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # 1. DagsHub / MLflow
    # --------------------------------------------------------

    dagshub.init(
        repo_owner="DurgaPrasad-237",
        repo_name="Ecom_Analytics_backend",
        mlflow=True
    )

    mlflow.set_experiment(
        "Demand Forecasting"
    )


    # --------------------------------------------------------
    # 2. Load data
    # --------------------------------------------------------

    print(
        "\nLoading data..."
    )

    orders = load_data(
        ORDERS_FILEPATH
    )

    products = load_data(
        PRODUCTS_FILEPATH
    )

    order_items = load_data(
        ORDER_ITEMS_FILEPATH
    )


    # --------------------------------------------------------
    # 3. Merge data
    # --------------------------------------------------------

    print(
        "\nMerging data..."
    )

    data = merge_dataframes(
        order_items,
        products,
        "product_id"
    )

    data = merge_dataframes(
        data,
        orders,
        "order_id"
    )


    # --------------------------------------------------------
    # 4. Feature engineering
    # --------------------------------------------------------

    print(
        "\nCreating daily demand..."
    )

    daily_demand = (
        create_daily_demand_dataframe(
            data
        )
    )

    print(
        f"Daily demand shape: "
        f"{daily_demand.shape}"
    )


    # --------------------------------------------------------
    # 5. Get 2025 test data
    # --------------------------------------------------------

    X_test, y_test = get_test_data(
        daily_demand
    )

    print(
        f"\n2025 test rows: "
        f"{len(X_test)}"
    )


    # --------------------------------------------------------
    # 6. Get all models
    # --------------------------------------------------------

    model_files = get_model_files()

    print(
        f"\nModels found: "
        f"{len(model_files)}"
    )

    for model_file in model_files:

        print(
            f"  - {model_file.name}"
        )


    # --------------------------------------------------------
    # 7. Evaluate
    # --------------------------------------------------------

    results = evaluate_models(
        model_files,
        X_test,
        y_test
    )


    # --------------------------------------------------------
    # 8. Sort by MAE
    # --------------------------------------------------------

    results = results.sort_values(
        "mae"
    ).reset_index(
        drop=True
    )


    # --------------------------------------------------------
    # 9. Save evaluation results
    # --------------------------------------------------------

    results_file = (
        RESULTS_DIR
        / "2025_model_evaluation.csv"
    )

    results.to_csv(
        results_file,
        index=False
    )

    # Save best model metrics for DVC
    metrics_file = RESULTS_DIR / "metrics.json"

    best_model = results.loc[
        results["rmse"].idxmin()
    ]

    metrics = {
        "model": best_model["model"],
        "mae": float(best_model["mae"]),
        "rmse": float(best_model["rmse"]),
        "r2": float(best_model["r2"]),
        "wape": float(best_model["wape"])
    }

    with open(metrics_file, "w") as f:
        import json
        json.dump(metrics, f, indent=4)


    # --------------------------------------------------------
    # 10. Display comparison
    # --------------------------------------------------------

    print(
        "\n========================================"
    )

    print(
        "       2025 MODEL EVALUATION"
    )

    print(
        "========================================"
    )

    print(
        results.to_string(
            index=False
        )
    )


    print(
        "\nEvaluation results saved to:"
    )

    print(
        results_file
    )


    # --------------------------------------------------------
    # 11. Show best model by each metric
    # --------------------------------------------------------

    best_mae = results.loc[
        results["mae"].idxmin()
    ]

    best_rmse = results.loc[
        results["rmse"].idxmin()
    ]

    best_r2 = results.loc[
        results["r2"].idxmax()
    ]

    best_wape = results.loc[
        results["wape"].idxmin()
    ]


    print(
        "\n========================================"
    )

    print(
        "       BEST MODEL BY METRIC"
    )

    print(
        "========================================"
    )

    print(
        f"Lowest MAE  : "
        f"{best_mae['model']} "
        f"({best_mae['mae']:.4f})"
    )

    print(
        f"Lowest RMSE : "
        f"{best_rmse['model']} "
        f"({best_rmse['rmse']:.4f})"
    )

    print(
        f"Highest R²  : "
        f"{best_r2['model']} "
        f"({best_r2['r2']:.4f})"
    )

    print(
        f"Lowest WAPE : "
        f"{best_wape['model']} "
        f"({best_wape['wape']:.2f}%)"
    )

    print(
        "========================================"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()