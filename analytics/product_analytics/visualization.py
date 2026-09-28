import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# KPI VISUALIZATIONS
# ============================================================

def visualization_total_units_sold(data):
    value = data["Total_Units_Sold"]

    fig, ax = plt.subplots(figsize=(6, 3))

    ax.text(
        0.5,
        0.5,
        f"{value:,}",
        ha="center",
        va="center",
        fontsize=32,
        fontweight="bold"
    )

    ax.text(
        0.5,
        0.2,
        "Total Units Sold",
        ha="center",
        va="center",
        fontsize=14
    )

    ax.axis("off")

    return fig


def visualization_total_revenue(data):
    value = data["Total_Revenue"]

    fig, ax = plt.subplots(figsize=(6, 3))

    ax.text(
        0.5,
        0.5,
        f"₹{value:,.0f}",
        ha="center",
        va="center",
        fontsize=30,
        fontweight="bold"
    )

    ax.text(
        0.5,
        0.2,
        "Total Revenue",
        ha="center",
        va="center",
        fontsize=14
    )

    ax.axis("off")

    return fig


def visualization_total_cost(data):
    value = data["Total_cost"]

    fig, ax = plt.subplots(figsize=(6, 3))

    ax.text(
        0.5,
        0.5,
        f"₹{value:,.0f}",
        ha="center",
        va="center",
        fontsize=30,
        fontweight="bold"
    )

    ax.text(
        0.5,
        0.2,
        "Total Cost",
        ha="center",
        va="center",
        fontsize=14
    )

    ax.axis("off")

    return fig


def visualization_total_profit(data):
    value = data["Total_Profit"]

    fig, ax = plt.subplots(figsize=(6, 3))

    ax.text(
        0.5,
        0.5,
        f"₹{value:,.0f}",
        ha="center",
        va="center",
        fontsize=30,
        fontweight="bold"
    )

    ax.text(
        0.5,
        0.2,
        "Total Profit",
        ha="center",
        va="center",
        fontsize=14
    )

    ax.axis("off")

    return fig


def visualization_profit_margin(data):
    value = data["Profit_Margin"]

    fig, ax = plt.subplots(figsize=(6, 3))

    ax.pie(
        [value, max(100 - value, 0)],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.35}
    )

    ax.text(
        0,
        0,
        f"{value:.2f}%",
        ha="center",
        va="center",
        fontsize=24,
        fontweight="bold"
    )

    ax.set_title("Profit Margin")

    return fig


def visualization_total_returns(data):
    value = data["Total Returns"]

    fig, ax = plt.subplots(figsize=(6, 3))

    ax.text(
        0.5,
        0.5,
        f"{value:,}",
        ha="center",
        va="center",
        fontsize=32,
        fontweight="bold"
    )

    ax.text(
        0.5,
        0.2,
        "Total Returns",
        ha="center",
        va="center",
        fontsize=14
    )

    ax.axis("off")

    return fig


def visualization_return_rate(data):
    value = data["Product return rate"]

    fig, ax = plt.subplots(figsize=(6, 3))

    ax.pie(
        [value, max(100 - value, 0)],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.35}
    )

    ax.text(
        0,
        0,
        f"{value:.2f}%",
        ha="center",
        va="center",
        fontsize=24,
        fontweight="bold"
    )

    ax.set_title("Product Return Rate")

    return fig


# ============================================================
# TOP PRODUCTS BY UNITS SOLD
# ============================================================

def visualization_top_10_products_sold(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    df = df.sort_values("quantity")

    ax.barh(
        df["product_name"],
        df["quantity"]
    )

    ax.set_title("Top 10 Products by Units Sold")
    ax.set_xlabel("Units Sold")
    ax.set_ylabel("Product")

    return fig


# ============================================================
# TOP CATEGORIES BY UNITS SOLD
# ============================================================

def visualization_top_10_categories_sold(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    df = df.sort_values("quantity")

    ax.barh(
        df["category"],
        df["quantity"]
    )

    ax.set_title("Top 10 Categories by Units Sold")
    ax.set_xlabel("Units Sold")
    ax.set_ylabel("Category")

    return fig


# ============================================================
# TOP PRODUCTS BY REVENUE
# ============================================================

def visualization_top_revenue_products(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    df = df.sort_values("item_revenue")

    ax.barh(
        df["product_name"],
        df["item_revenue"]
    )

    ax.set_title("Top 10 Products by Revenue")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Product")

    return fig


# ============================================================
# TOP CATEGORIES BY REVENUE
# ============================================================

def visualization_top_revenue_categories(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    df = df.sort_values("item_revenue")

    ax.barh(
        df["category"],
        df["item_revenue"]
    )

    ax.set_title("Top 10 Categories by Revenue")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Category")

    return fig


# ============================================================
# REVENUE CONTRIBUTION - PIE CHART
# ============================================================

def visualization_revenue_contribution_products(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        df["revenue_contribution_pct"],
        labels=df["product_name"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Revenue Contribution by Product")

    return fig


# ============================================================
# REVENUE CONTRIBUTION BY CATEGORY
# ============================================================

def visualization_revenue_contribution_categories(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        df["revenue_contribution_pct"],
        labels=df["category"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Revenue Contribution by Category")

    return fig


# ============================================================
# TOP PROFIT PRODUCTS
# ============================================================

def visualization_top_profit_products(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    df = df.sort_values("profit")

    ax.barh(
        df["product_name"],
        df["profit"]
    )

    ax.set_title("Top 10 Products by Profit")
    ax.set_xlabel("Profit")
    ax.set_ylabel("Product")

    return fig


# ============================================================
# PROFIT CONTRIBUTION
# ============================================================

def visualization_profit_contribution(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        df["profit_contribution_pct"],
        labels=df["product_name"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Profit Contribution by Product")

    return fig


# ============================================================
# TOP LOSS PRODUCTS
# ============================================================

def visualization_top_loss_products(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    df = df.sort_values("profit")

    ax.barh(
        df["product_name"],
        df["profit"]
    )

    ax.set_title("Top Loss-Making Products")
    ax.set_xlabel("Profit / Loss")
    ax.set_ylabel("Product")

    return fig


# ============================================================
# RETURN RATE BY PRODUCT
# ============================================================

def visualization_return_rate_products(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    df = df.sort_values("return_rate_pct")

    ax.barh(
        df["product_name"],
        df["return_rate_pct"]
    )

    ax.set_title("Top 10 Products by Return Rate")
    ax.set_xlabel("Return Rate (%)")
    ax.set_ylabel("Product")

    return fig


# ============================================================
# PRODUCT RATING VS RETURN RATE
# ============================================================

def visualization_rating_vs_return_rate(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        df["avg_rating"],
        df["return_rate_pct"]
    )

    ax.set_title("Product Rating vs Return Rate")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Return Rate (%)")

    return fig


# ============================================================
# MONTHLY PRODUCT TREND
# ============================================================

def visualization_monthly_product_trend(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(12, 6))

    for year in sorted(df["year"].unique()):

        year_df = df[df["year"] == year].sort_values("month")

        ax.plot(
            year_df["month"],
            year_df["item_revenue"],
            marker="o",
            linewidth=2,
            label=str(year)
        )

    ax.set_title(
        "Monthly Revenue Trend",
        fontsize=16
    )

    ax.set_xlabel("Month")

    ax.set_ylabel("Revenue")

    ax.set_xticks(range(1, 13))

    ax.set_xticklabels([
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ])

    ax.ticklabel_format(
        style="sci",
        axis="y",
        scilimits=(6, 6)
    )

    ax.legend(
        title="Year"
    )

    ax.grid(
        axis="y",
        alpha=0.3
    )

    plt.tight_layout()

    return fig


# ============================================================
# PRODUCT PERFORMANCE
# ============================================================

def visualization_product_performance(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        df["product_name"],
        df["revenue"]
    )

    ax.set_title("Product Performance - Revenue")
    ax.set_xlabel("Product")
    ax.set_ylabel("Revenue")

    plt.xticks(rotation=45, ha="right")

    return fig


# ============================================================
# PRODUCT PERFORMANCE - PROFIT MARGIN
# ============================================================

def visualization_product_profit_margin(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        df["product_name"],
        df["profit_margin_pct"]
    )

    ax.set_title("Product Profit Margin")
    ax.set_xlabel("Product")
    ax.set_ylabel("Profit Margin (%)")

    plt.xticks(rotation=45, ha="right")

    return fig


# ============================================================
# PRODUCT PERFORMANCE - REVENUE VS PROFIT
# ============================================================

def visualization_revenue_vs_profit(data):

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.scatter(
        df["revenue"],
        df["profit"]
    )

    ax.set_title("Revenue vs Profit by Product")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Profit")

    return fig