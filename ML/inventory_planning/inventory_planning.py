# ML/InventoryPlanning/inventory_planning.py

import pandas as pd
from pathlib import Path


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

FORECAST_FILE = (
    BASE_DIR
    / "ML"
    / "DemandForecasting"
    / "results"
    / "2026_demand_forecast.csv"
)

RESULTS_DIR = (
    BASE_DIR
    / "ML"
    / "inventory_planning"
    / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 2. INVENTORY PARAMETERS
# ============================================================

# Assumed supplier lead time
LEAD_TIME_DAYS = 7

# Safety stock as percentage of lead-time demand
SAFETY_STOCK_PERCENT = 0.20


# ============================================================
# 3. LOAD FORECAST
# ============================================================

print("Loading 2026 demand forecast...")

forecast = pd.read_csv(
    FORECAST_FILE
)

forecast["forecast_date"] = pd.to_datetime(
    forecast["forecast_date"]
)

print(
    f"Forecast rows: {len(forecast):,}"
)


# ============================================================
# 4. PRODUCT-LEVEL FORECAST SUMMARY
# ============================================================

product_summary = (
    forecast
    .groupby("product_name")
    .agg(
        total_forecast_demand=(
            "forecast_demand",
            "sum"
        ),

        average_daily_demand=(
            "forecast_demand",
            "mean"
        ),

        maximum_daily_demand=(
            "forecast_demand",
            "max"
        )
    )
    .reset_index()
)


# ============================================================
# 5. LEAD-TIME DEMAND
# ============================================================

product_summary["lead_time_demand"] = (
    product_summary["average_daily_demand"]
    * LEAD_TIME_DAYS
)


# ============================================================
# 6. SAFETY STOCK
# ============================================================

product_summary["safety_stock"] = (
    product_summary["lead_time_demand"]
    * SAFETY_STOCK_PERCENT
)


# ============================================================
# 7. REORDER POINT
# ============================================================

product_summary["reorder_point"] = (
    product_summary["lead_time_demand"]
    + product_summary["safety_stock"]
)


# ============================================================
# 8. RECOMMENDED INVENTORY
# ============================================================

product_summary["recommended_inventory"] = (
    product_summary["reorder_point"]
)


# ============================================================
# 9. ROUND INVENTORY VALUES
# ============================================================

inventory_columns = [
    "total_forecast_demand",
    "average_daily_demand",
    "maximum_daily_demand",
    "lead_time_demand",
    "safety_stock",
    "reorder_point",
    "recommended_inventory"
]

product_summary[inventory_columns] = (
    product_summary[inventory_columns]
    .round(2)
)


# ============================================================
# 10. SAVE INVENTORY PLAN
# ============================================================

output_file = (
    RESULTS_DIR
    / "inventory_plan_2026.csv"
)

product_summary.to_csv(
    output_file,
    index=False
)


# ============================================================
# 11. DISPLAY RESULTS
# ============================================================

print()
print("=" * 60)
print("INVENTORY PLANNING COMPLETED")
print("=" * 60)

print(
    f"Products analyzed: "
    f"{len(product_summary):,}"
)

print(
    f"Lead time: "
    f"{LEAD_TIME_DAYS} days"
)

print(
    f"Safety stock: "
    f"{SAFETY_STOCK_PERCENT * 100:.0f}% "
    f"of lead-time demand"
)

print(
    f"Saved to: "
    f"{output_file}"
)

print("=" * 60)

print()
print("Sample inventory plan:")

print(
    product_summary.head(10)
)