import pandas as pd
import numpy as np

def sales_kpis(df: pd.DataFrame) -> dict:

    gross_revenue = df["item_revenue"].sum()
    gross_profit = df["profit"].sum()
    refund_amount = df["refund_amount"].sum()
    total_item_cost = df["item_cost"].sum()

    profit_margin = (
        (gross_profit / gross_revenue) * 100
        if gross_revenue != 0 else 0
    )

    net_revenue = gross_revenue - refund_amount

    return {
        "Gross_Revenue": gross_revenue,
        "Gross_Profit": gross_profit,
        "Profit_Margin": profit_margin,
        "Refund_Amount": refund_amount,
        "Net_Revenue": net_revenue,
        "Total_Item_Cost": total_item_cost
    }

def product_profitability_analysis(df: pd.DataFrame):

    result = (
        df.groupby("product_name")
        .agg(
            revenue=("item_revenue", "sum"),
            profit=("profit", "sum"),
            item_cost=("item_cost", "sum"),
            avg_discount=("discount_percentage", "mean"),
            number_of_times_discount_applied=(
                "discount_percentage",
                lambda x: (x > 0).sum()
            )
        )
        .reset_index()
    )

    result["profit_margin"] = (
        result["profit"] / result["revenue"]
    ) * 100

    return result

def loss_making_order_rate(df:pd.DataFrame):
    # First calculate total order-item records per product:
    product_order_counts = (
        df
        .groupby("product_name")
        .size()
        .reset_index(name="total_order_items")
    )
    # Calculate loss-making order count:
    loss_order_counts = (
        df[
            df["item_revenue"] < df["item_cost"]
        ]
        .groupby("product_name")
        .size()
        .reset_index(name="loss_making_order_count")
    )

    loss_making_order_analysis = product_order_counts.merge(
        loss_order_counts,
        on="product_name",
        how="left"
    )
    # prodcut wiht no loss makign orders
    loss_making_order_analysis["loss_making_order_count"] = (
        loss_making_order_analysis["loss_making_order_count"]
        .fillna(0)
    )
    # calcula rate
    loss_making_order_analysis["loss_making_order_rate"] = (
        loss_making_order_analysis["loss_making_order_count"]
        / loss_making_order_analysis["total_order_items"]
    ) * 100

    # top loss makimg order rate
    top_loss_making_order_rate = (
        loss_making_order_analysis
        .sort_values("loss_making_order_rate", ascending=False)
        .head(10)
    )

    return top_loss_making_order_rate



def monthly_revenue_by_year(df: pd.DataFrame):

    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    monthly_revenue = (
        df
        .groupby(["year", "month"], observed=True)["item_revenue"]
        .sum()
        .reset_index()
    )

    monthly_revenue["month"] = pd.Categorical(
        monthly_revenue["month"],
        categories=month_order,
        ordered=True
    )

    monthly_revenue = monthly_revenue.sort_values(
        ["year", "month"]
    )

    return monthly_revenue.to_dict(orient="records")


def monthly_profit_by_year(df: pd.DataFrame):

    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    monthly_profit = (
        df
        .groupby(["year", "month"], observed=True)["profit"]
        .sum()
        .reset_index()
    )

    monthly_profit["month"] = pd.Categorical(
        monthly_profit["month"],
        categories=month_order,
        ordered=True
    )

    monthly_profit = monthly_profit.sort_values(["year", "month"])

    return monthly_profit.to_dict(orient="records")