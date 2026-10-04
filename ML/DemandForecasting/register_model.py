from pathlib import Path

import dagshub
import joblib
import mlflow
import mlflow.sklearn

from mlflow.models import infer_signature


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
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_FILE = (
    BASE_DIR
    / "ML"
    / "DemandForecasting"
    / "models"
    / "final_demand_forecasting_elasticnet.pkl"
)


# ============================================================
# Existing trained model
# ============================================================

print("Loading existing final model...")

model = joblib.load(MODEL_FILE)

print("Model loaded successfully.")


# ============================================================
# Model input example
# ============================================================

input_example = {
    "product_name": "Example Product",
    "year": 2025,
    "month": 12,
    "day_of_week": 1,
    "week_of_year": 50,
    "quarter": 4,
    "lag_1": 5.0,
    "lag_7": 6.0,
    "lag_14": 5.0,
    "lag_28": 7.0,
    "rolling_mean_7": 5.5,
    "rolling_mean_14": 5.8,
    "rolling_mean_28": 6.0,
}


import pandas as pd

input_df = pd.DataFrame([input_example])


# ============================================================
# Generate prediction for signature
# ============================================================

prediction = model.predict(input_df)


# ============================================================
# Infer model signature
# ============================================================

signature = infer_signature(
    input_df,
    prediction
)


# ============================================================
# New registered model name
# ============================================================

MODEL_NAME = "DemandForecastingModel"


# ============================================================
# Register model with signature
# ============================================================

with mlflow.start_run(
    run_name="register_final_elasticnet"
):

    mlflow.log_params({
        "model": "ElasticNet",
        "alpha": 0.01,
        "l1_ratio": 0.9,
        "max_iter": 10000,
        "training_period": "2023-2025"
    })

    mlflow.set_tags({
        "stage": "production",
        "model_status": "final",
        "model_type": "ElasticNet",
        "training_period": "2023-2025",
        "selection_basis": "2025_holdout_evaluation"
    })

    mlflow.set_tag(
        "description",
        "Final ElasticNet demand forecasting model selected after 2025 evaluation."
    )

    mlflow.sklearn.log_model(
        sk_model=model,
        name="elasticnet_demand_forecasting",
        signature=signature,
        input_example=input_df,
        registered_model_name=MODEL_NAME
    )

    run_id = mlflow.active_run().info.run_id

    print("\nModel registered successfully.")
    print("Run ID:", run_id)
    print("Model:", MODEL_NAME)


# ============================================================
# Update registered model metadata
# ============================================================

client = mlflow.MlflowClient()

client.update_registered_model(
    name=MODEL_NAME,
    description=(
        "Final ElasticNet demand forecasting model trained on "
        "2023-2025 data. Selected based on 2025 holdout evaluation. "
        "Hyperparameters: alpha=0.01, l1_ratio=0.9."
    )
)


# ============================================================
# Get latest version
# ============================================================

versions = client.search_model_versions(
    f"name='{MODEL_NAME}'"
)

latest_version = max(
    versions,
    key=lambda v: int(v.version)
)

version_number = latest_version.version


# ============================================================
# Add version tags
# ============================================================

client.set_model_version_tag(
    name=MODEL_NAME,
    version=version_number,
    key="model_type",
    value="ElasticNet"
)

client.set_model_version_tag(
    name=MODEL_NAME,
    version=version_number,
    key="alpha",
    value="0.01"
)

client.set_model_version_tag(
    name=MODEL_NAME,
    version=version_number,
    key="l1_ratio",
    value="0.9"
)

client.set_model_version_tag(
    name=MODEL_NAME,
    version=version_number,
    key="training_period",
    value="2023-2025"
)

client.set_model_version_tag(
    name=MODEL_NAME,
    version=version_number,
    key="status",
    value="production"
)


# ============================================================
# Set production alias
# ============================================================

client.set_registered_model_alias(
    MODEL_NAME,
    "production",
    version_number
)


print("\n========================================")
print("FINAL MODEL REGISTRATION COMPLETE")
print("========================================")
print("Model:", MODEL_NAME)
print("Version:", version_number)
print("Alias: production")
print("Model type: ElasticNet")
print("Alpha: 0.01")
print("L1 ratio: 0.9")
print("Training period: 2023-2025")
print("Signature: created")