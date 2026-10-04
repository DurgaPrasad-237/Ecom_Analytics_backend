import time
import joblib
import mlflow
import dagshub
import pandas as pd
import numpy as np

from pathlib import Path

from ML.DemandForecasting.feature_engineering import (
    periods,
    lag_features,
    rolling_features
)

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso,
    ElasticNet
)

from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import (
    HistGradientBoostingRegressor
)

from xgboost import XGBRegressor

from sklearn.model_selection import (
    TimeSeriesSplit,
    GridSearchCV,
    RandomizedSearchCV
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
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

MODEL_DIR = BASE_DIR / "ML"/ "DemandForecasting" /"models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_DIR = BASE_DIR / "ML"/ "DemandForecasting" /"results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# DATA LOADING
# ============================================================

def load_data(file_path: str) -> pd.DataFrame:

    return pd.read_csv(file_path)


# ============================================================
# DATA MERGING
# ============================================================

def merge_dataframes(
    first_df: pd.DataFrame,
    second_df: pd.DataFrame,
    on: str
) -> pd.DataFrame:

    return first_df.merge(
        second_df,
        on=on,
        how="left"
    )


# ============================================================
# DAILY DEMAND + FEATURE ENGINEERING
# ============================================================

def creates_daily_demand_dataframe(
    df: pd.DataFrame
) -> pd.DataFrame:

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

    # Create continuous daily time series
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
# TIME-BASED TRAIN / TEST SPLIT
# ============================================================

def split_data_according_to_time(
    df: pd.DataFrame,
    train_end: int,
    test_year: int
):

    train = df[
        df["year"] < train_end
    ]

    test = df[
        df["year"] == test_year
    ]

    X_train = train.drop(
        columns=[
            "quantity",
            "order_date"
        ]
    )

    y_train = train["quantity"]

    X_test = test.drop(
        columns=[
            "quantity",
            "order_date"
        ]
    )

    y_test = test["quantity"]

    return (
        X_train,
        y_train,
        X_test,
        y_test
    )


# ============================================================
# FEATURES
# ============================================================

def get_num_cat_features(
    df: pd.DataFrame
):

    categorical_features = [
        "product_name"
    ]

    numerical_features = [
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

    return (
        categorical_features,
        numerical_features
    )


# ============================================================
# PREPROCESSOR
# ============================================================

def create_preprocessor(
    categorical_features: list,
    numerical_features: list
):

    categorical_transformer = Pipeline(
        steps=[
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    numerical_transformer = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler()
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                categorical_transformer,
                categorical_features
            ),
            (
                "num",
                numerical_transformer,
                numerical_features
            )
        ]
    )

    return preprocessor


# ============================================================
# PIPELINE
# ============================================================

def create_model_pipeline(
    preprocessor,
    model
):

    return Pipeline(
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
# BASELINE MODELS
# ============================================================

def get_baseline_models(
    preprocessor
):

    models = {

        "linear_regression":
            create_model_pipeline(
                preprocessor,
                LinearRegression()
            ),

        "ridge":
            create_model_pipeline(
                preprocessor,
                Ridge(
                    alpha=1.0
                )
            ),

        "lasso":
            create_model_pipeline(
                preprocessor,
                Lasso(
                    alpha=0.01,
                    max_iter=10000
                )
            ),

        "decision_tree":
            create_model_pipeline(
                preprocessor,
                DecisionTreeRegressor(
                    random_state=42
                )
            ),

        "xgboost":
            create_model_pipeline(
                preprocessor,
                XGBRegressor(
                    n_estimators=200,
                    learning_rate=0.05,
                    max_depth=6,
                    random_state=42,
                    n_jobs=-1
                )
            ),

        "elasticnet":
            create_model_pipeline(
                preprocessor,
                ElasticNet(
                    alpha=0.01,
                    l1_ratio=0.9,
                    max_iter=10000
                )
            )
    }

    return models


# ============================================================
# BASELINE CV EVALUATION
# ============================================================

def evaluate_cv(
    model,
    X_train,
    y_train,
    tscv
):

    scores = GridSearchCV(
        estimator=model,
        param_grid={},
        cv=tscv,
        scoring="neg_mean_absolute_error",
        n_jobs=-1
    )

    scores.fit(
        X_train,
        y_train
    )

    return -scores.best_score_


# ============================================================
# TEST METRICS
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

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2
    }


# ============================================================
# BASELINE EXPERIMENTS
# ============================================================

def run_baseline_experiments(
    models,
    X_train,
    y_train,
    tscv
):

    results = []

    for model_name, model in models.items():

        print(
            f"\nTraining baseline: {model_name}"
        )

        start_time = time.time()

        with mlflow.start_run(
            run_name=f"{model_name}_baseline"
        ):

            cv_mae = evaluate_cv(
                model,
                X_train,
                y_train,
                tscv
            )

            model.fit(
                X_train,
                y_train
            )

            training_time = (
                time.time() - start_time
            )

            # --------------------------------------------
            # Save EVERY baseline model
            # --------------------------------------------

            model_file = (
                MODEL_DIR
                / f"{model_name}_baseline.pkl"
            )

            joblib.dump(
                model,
                model_file
            )

            # --------------------------------------------
            # Log model artifact to MLflow
            # --------------------------------------------

            mlflow.log_artifact(
                str(model_file)
            )

            mlflow.log_param(
                "model",
                model_name
            )

            mlflow.log_param(
                "experiment_type",
                "baseline"
            )

            mlflow.log_metric(
                "cv_mae",
                cv_mae
            )

            mlflow.log_metric(
                "training_time_seconds",
                training_time
            )

            results.append(
                {
                    "model": model_name,
                    "experiment": "baseline",
                    "cv_mae": cv_mae,
                    "training_time_seconds":
                        training_time
                }
            )

            print(
                f"CV MAE: {cv_mae:.4f}"
            )

    return pd.DataFrame(results)


# ============================================================
# HYPERPARAMETER SEARCH CONFIGURATION
# ============================================================

def get_tuning_configs(
    preprocessor
):

    configs = {

        "ridge_tuned": {
            "search_type": "grid",

            "pipeline":
                create_model_pipeline(
                    preprocessor,
                    Ridge()
                ),

            "params": {
                "model__alpha": [
                    0.01,
                    0.1,
                    1,
                    10,
                    25,
                    50,
                    75,
                    100,
                    150,
                    200,
                    500,
                    1000
                ]
            }
        },

        "elasticnet_tuned": {
            "search_type": "grid",

            "pipeline":
                create_model_pipeline(
                    preprocessor,
                    ElasticNet(
                        max_iter=10000
                    )
                ),

            "params": {
                "model__alpha": [
                    0.001,
                    0.01,
                    0.1,
                    1,
                    10,
                    100
                ],

                "model__l1_ratio": [
                    0.1,
                    0.3,
                    0.5,
                    0.7,
                    0.9
                ]
            }
        },

        "xgboost_tuned": {
            "search_type": "random",

            "pipeline":
                create_model_pipeline(
                    preprocessor,
                    XGBRegressor(
                        random_state=42,
                        n_jobs=-1
                    )
                ),

            "params": {

                "model__n_estimators": [
                    100,
                    200,
                    300,
                    500
                ],

                "model__learning_rate": [
                    0.01,
                    0.03,
                    0.05,
                    0.1
                ],

                "model__max_depth": [
                    3,
                    5,
                    6,
                    8,
                    10
                ],

                "model__subsample": [
                    0.7,
                    0.8,
                    1.0
                ],

                "model__colsample_bytree": [
                    0.7,
                    0.8,
                    1.0
                ]
            }
        }
    }

    return configs


# ============================================================
# HYPERPARAMETER TUNING
# ============================================================

def run_hyperparameter_tuning(
    configs,
    X_train,
    y_train,
    tscv
):

    results = []

    best_models = {}

    for name, config in configs.items():

        print(
            f"\nTuning: {name}"
        )

        start_time = time.time()

        if config["search_type"] == "grid":

            search = GridSearchCV(
                estimator=config["pipeline"],
                param_grid=config["params"],
                cv=tscv,
                scoring="neg_mean_absolute_error",
                n_jobs=-1,
                verbose=1
            )

        else:

            search = RandomizedSearchCV(
                estimator=config["pipeline"],
                param_distributions=config["params"],
                n_iter=20,
                cv=tscv,
                scoring="neg_mean_absolute_error",
                n_jobs=-1,
                random_state=42,
                verbose=1
            )

        with mlflow.start_run(
            run_name=name
        ):

            search.fit(
                X_train,
                y_train
            )

            training_time = (
                time.time() - start_time
            )

            best_cv_mae = (
                -search.best_score_
            )

            mlflow.log_param(
                "model",
                name
            )

            mlflow.log_param(
                "search_type",
                config["search_type"]
            )

            mlflow.log_metric(
                "cv_mae",
                best_cv_mae
            )

            mlflow.log_metric(
                "training_time_seconds",
                training_time
            )

            # Log best parameters
            for param_name, value in (
                search.best_params_.items()
            ):

                mlflow.log_param(
                    param_name,
                    value
                )

            # Save tuned model
            model_file = (
                MODEL_DIR
                / f"{name}.pkl"
            )

            joblib.dump(
                search.best_estimator_,
                model_file
            )

            # Log model artifact
            mlflow.log_artifact(
                str(model_file)
            )

            results.append(
                {
                    "model": name,
                    "experiment": "tuned",
                    "cv_mae": best_cv_mae,
                    "training_time_seconds":
                        training_time,
                    "best_params":
                        search.best_params_
                }
            )

            best_models[name] = (
                search.best_estimator_
            )

            print(
                f"Best CV MAE: "
                f"{best_cv_mae:.4f}"
            )

            print(
                f"Best parameters: "
                f"{search.best_params_}"
            )

    return (
        pd.DataFrame(results),
        best_models
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # 1. Start DagsHub / MLflow
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

    print("\nLoading data...")

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

    print("\nMerging data...")

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

    print("\nCreating daily demand...")

    daily_demand = (
        creates_daily_demand_dataframe(
            data
        )
    )

    print(
        f"Daily demand shape: "
        f"{daily_demand.shape}"
    )


    # --------------------------------------------------------
    # 5. Train / test split
    # --------------------------------------------------------

    X_train, y_train, X_test, y_test = (
        split_data_according_to_time(
            daily_demand,
            train_end=2025,
            test_year=2025
        )
    )


    print(
        f"\nTraining rows: "
        f"{len(X_train)}"
    )

    print(
        f"Test rows: "
        f"{len(X_test)}"
    )


    # --------------------------------------------------------
    # 6. Features
    # --------------------------------------------------------

    (
        categorical_features,
        numerical_features
    ) = get_num_cat_features(
        X_train
    )


    # --------------------------------------------------------
    # 7. Preprocessor
    # --------------------------------------------------------

    preprocessor = create_preprocessor(
        categorical_features,
        numerical_features
    )


    # --------------------------------------------------------
    # 8. Time Series CV
    # --------------------------------------------------------

    tscv = TimeSeriesSplit(
        n_splits=5
    )


    # --------------------------------------------------------
    # 9. Baseline models
    # --------------------------------------------------------

    print(
        "\n=============================="
    )

    print(
        "BASELINE EXPERIMENTS"
    )

    print(
        "=============================="
    )

    baseline_models = (
        get_baseline_models(
            preprocessor
        )
    )

    baseline_results = (
        run_baseline_experiments(
            baseline_models,
            X_train,
            y_train,
            tscv
        )
    )


    # --------------------------------------------------------
    # 10. Hyperparameter tuning
    # --------------------------------------------------------

    print(
        "\n=============================="
    )

    print(
        "HYPERPARAMETER TUNING"
    )

    print(
        "=============================="
    )

    tuning_configs = (
        get_tuning_configs(
            preprocessor
        )
    )

    (
        tuned_results,
        tuned_models
    ) = run_hyperparameter_tuning(
        tuning_configs,
        X_train,
        y_train,
        tscv
    )


    # --------------------------------------------------------
    # 11. Combine experiment results
    # --------------------------------------------------------

    all_results = pd.concat(
        [
            baseline_results,
            tuned_results
        ],
        ignore_index=True
    )

    all_results = all_results.sort_values(
        "cv_mae"
    ).reset_index(
        drop=True
    )


   

    # --------------------------------------------------------
    # 12. Save comparison
    # --------------------------------------------------------

    results_file = (
        RESULTS_DIR
        / "model_comparison.csv"
    )

    all_results.to_csv(
        results_file,
        index=False
    )

    print(
        f"\nModel comparison saved to:"
    )

    print(
        results_file
    )

    print(
        "\nTraining pipeline completed."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()