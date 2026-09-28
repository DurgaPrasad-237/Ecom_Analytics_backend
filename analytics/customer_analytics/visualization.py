import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from analytics.customer_analytics.analysis import (
    get_monthly_signup_by_gender,
    get_monthly_signup_counts,
    customer_signup_yearwise_trend,
    customer_churn_analysis
)


def visualization_monthly_signup_gender(result):

    # result = get_monthly_signup_by_gender(df)
    result = pd.DataFrame(result)

    fig, ax = plt.subplots(figsize=(15, 6))

    sns.barplot(
        data=result,
        x="customer_signup_month",
        y="count",
        hue="gender",
        estimator="sum",
        errorbar=None,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)

    ax.set_title("Customer Signups by Month and Gender")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Customers")

    return fig


def visualization_monthly_signup(result):

    # result = get_monthly_signup_counts(df)
    result = pd.DataFrame(result)

    fig, ax = plt.subplots(figsize=(15, 6))

    sns.barplot(
        data=result,
        x="customer_signup_month",
        y="count",
        hue="customer_signup_month",
        palette="viridis",
        errorbar=None,
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)

    ax.set_title("Customer Signups by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Customers")

    return fig


def visualization_signup_trend_yearwise(result):

    # result = customer_signup_yearwise_trend(df)
    result = pd.DataFrame(result)

    fig, ax = plt.subplots(figsize=(15, 6))

    sns.lineplot(
        data=result,
        x="month",
        y="count",
        hue="customer_signup_year",
        style="customer_signup_year",
        marker="o",
        ax=ax
    )

    ax.set_title("Customer Signup Trend by Year")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Customers")

    return fig


def visualization_churn(result):

    # result = customer_churn_analysis(df)
    result = pd.DataFrame(result)

    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(
        data=result,
        x="customer_status",
        y="count",
        errorbar=None,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)

    ax.set_title("Customer Status Distribution")
    ax.set_xlabel("Customer Status")
    ax.set_ylabel("Number of Customers")

    return fig


def visualization_customer_segment(result):

    # result = customer_churn_analysis(df)
    result = pd.DataFrame(result)

    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(
        data=result,
        x="customer_segment",
        y="count",
        errorbar=None,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)

    ax.set_title("Customer Segment Distribution")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Number of Customers")

    return fig


def Visualization_Average_Spend_by_Customer_Segment(result):
    result = pd.DataFrame(result)
    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(
        data=result,
        x="customer_segment",
        y="total_spend_mean"
    )

    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3)

    ax.set_title("Average Customer Spend by Segment")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Average Spend")


    return fig

def Visualization_total_spending_by_customer_segment(result):
    result = pd.DataFrame(result)
    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(
        data=result,
        x="customer_segment",
        y="total_sum"
    )

    ax.set_title("Total Spending by Customer Segment")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Total Spending")

    return fig


def Visualization_customer_count_by_segment(result):
    result = pd.DataFrame(result)
    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(
        data=result,
        x="customer_segment",
        y="cust_count"
    )

    ax.set_title("Customer Count by Segment")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Number of Customers")

    return fig


def Visualization_avg_vs_median_spend(result):
    result = pd.DataFrame(result)
   

    mean_median_df = result.melt(
        id_vars="customer_segment",
        value_vars=[
            "total_spend_mean",
            "total_spend_median"
        ],
        var_name="spend_type",
        value_name="spend"
    )
    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(
        data=mean_median_df,
        x="customer_segment",
        y="spend",
        hue="spend_type"
    )

    ax.set_title("Average vs Median Customer Spend")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Spend")

    return fig


def Visualization_spend_distirubtion_by_segment(result):
    result = pd.DataFrame(result)
    fig, ax = plt.subplots(figsize=(12, 7))

    sns.boxplot(
        data=result,
        x="customer_segment",
        y="total_spend"
    )

    ax.set_title("Customer Spending Distribution by Segment")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Total Spend")

    return fig


def Visualization_coeff_of_variation_by_segment(result):
    result = pd.DataFrame(result)
    fig, ax = plt.subplots(figsize=(12, 7))

    sns.barplot(
        data=result,
        x="customer_segment",
        y="cv"
    )

    ax.set_title("Spending Variation by Customer Segment")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Coefficient of Variation (%)")

    return fig