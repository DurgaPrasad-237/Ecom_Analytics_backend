import streamlit as st

from app.api_client import (
    get_total_units_sold,
    get_total_revenue,
    get_total_profit,
    get_total_product_cost,
    get_profit_margin,
    get_total_returns,
    get_product_return_rate,
    get_top_10_products_sold,
    get_top_10_categories_sold,
    get_top_10_revenue_products,
    get_top_10_revenue_categories,
    get_top_profit_products,
    get_top_loss_products,
    get_top_return_rate_products,
    get_monthly_product_trend,
    get_product_performance,
)

from analytics.product_analytics.visualization import (
    visualization_total_units_sold,
    visualization_total_revenue,
    visualization_total_cost,
    visualization_total_profit,
    visualization_profit_margin,
    visualization_total_returns,
    visualization_return_rate,
    visualization_top_10_products_sold,
    visualization_top_10_categories_sold,
    visualization_top_revenue_products,
    visualization_top_revenue_categories,
    visualization_revenue_contribution_products,
    visualization_revenue_contribution_categories,
    visualization_top_profit_products,
    visualization_profit_contribution,
    visualization_top_loss_products,
    visualization_return_rate_products,
    visualization_rating_vs_return_rate,
    visualization_monthly_product_trend,
    visualization_product_performance,
    visualization_product_profit_margin,
    visualization_revenue_vs_profit,
)

from components.chat import analytics_chat


def product_page():

    st.title("Product Analytics")

    st.caption(
        "Analyze product sales, revenue, profit, costs, returns, and performance."
    )

    # =========================================================
    # GET DATA FROM FASTAPI
    # =========================================================

    try:

        total_units = get_total_units_sold()

        total_revenue = get_total_revenue()

        total_profit = get_total_profit()

        total_cost = get_total_product_cost()

        profit_margin = get_profit_margin()

        total_returns = get_total_returns()

        return_rate = get_product_return_rate()

        top_products_sold = get_top_10_products_sold()

        top_categories_sold = get_top_10_categories_sold()

        top_revenue_products = get_top_10_revenue_products()

        top_revenue_categories = get_top_10_revenue_categories()

        top_profit = get_top_profit_products()

        top_loss = get_top_loss_products()

        top_return_rate = get_top_return_rate_products()

        product_performance = get_product_performance()

    except Exception as e:

        st.error(
            "Could not connect to FastAPI. "
            "Make sure FastAPI is running on port 8000."
        )

        st.exception(e)

        return

    # =========================================================
    # KPI CARDS
    # =========================================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Units Sold",
        f"{total_units['Total_Units_Sold']:,}"
    )

    col2.metric(
        "Total Revenue",
        f"₹{total_revenue['Total_Revenue']:,.0f}"
    )

    col3.metric(
        "Total Profit",
        f"₹{total_profit['Total_Profit']:,.0f}"
    )

    col4.metric(
        "Total Cost",
        f"₹{total_cost['Total_cost']:,.0f}"
    )

    st.divider()

    # =========================================================
    # PROFIT MARGIN / RETURNS
    # =========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("Profit Margin")

        fig = visualization_profit_margin(
            profit_margin
        )

        st.pyplot(fig, width="stretch")

    with col2:

        st.subheader("Total Returns")

        fig = visualization_total_returns(
            total_returns
        )

        st.pyplot(fig, width="stretch")

    with col3:

        st.subheader("Product Return Rate")

        fig = visualization_return_rate(
            return_rate
        )

        st.pyplot(fig, width="stretch")

    st.divider()

    # =========================================================
    # SALES ANALYSIS
    # =========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top 10 Products by Units Sold")

        fig = visualization_top_10_products_sold(
            top_products_sold
        )

        st.pyplot(fig, width="stretch")

    with col2:

        st.subheader("Top 10 Categories by Units Sold")

        fig = visualization_top_10_categories_sold(
            top_categories_sold
        )

        st.pyplot(fig, width="stretch")

    # =========================================================
    # REVENUE ANALYSIS
    # =========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top 10 Products by Revenue")

        fig = visualization_top_revenue_products(
            top_revenue_products
        )

        st.pyplot(fig, width="stretch")

    with col2:

        st.subheader("Top 10 Categories by Revenue")

        fig = visualization_top_revenue_categories(
            top_revenue_categories
        )

        st.pyplot(fig, width="stretch")

    # =========================================================
    # REVENUE CONTRIBUTION
    # =========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Revenue Contribution by Product")

        fig = visualization_revenue_contribution_products(
            top_revenue_products
        )

        st.pyplot(fig, width="stretch")

    with col2:

        st.subheader("Revenue Contribution by Category")

        fig = visualization_revenue_contribution_categories(
            top_revenue_categories
        )

        st.pyplot(fig, width="stretch")

    # =========================================================
    # PROFIT ANALYSIS
    # =========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top Profit Products")

        fig = visualization_top_profit_products(
            top_profit
        )

        st.pyplot(fig, width="stretch")

    with col2:

        st.subheader("Profit Contribution")

        fig = visualization_profit_contribution(
            top_profit
        )

        st.pyplot(fig, width="stretch")

    # =========================================================
    # PRODUCT ANALYSIS DROPDOWN
    # =========================================================

    st.divider()

    st.subheader("Detailed Product Analysis")

    option = st.selectbox(
        "Select Analysis",
        (
            "Top Loss-Making Products",
            "Products with Highest Return Rate",
            "Rating vs Return Rate",
            "Product Performance",
            "Product Profit Margin",
            "Revenue vs Profit"
        )
    )

    if option == "Top Loss-Making Products":

        fig = visualization_top_loss_products(
            top_loss
        )

        st.pyplot(fig, width="stretch")

    elif option == "Products with Highest Return Rate":

        fig = visualization_return_rate_products(
            top_return_rate
        )

        st.pyplot(fig, width="stretch")

    elif option == "Rating vs Return Rate":

        fig = visualization_rating_vs_return_rate(
            top_return_rate
        )

        st.pyplot(fig, width="stretch")

    elif option == "Product Performance":

        fig = visualization_product_performance(
            product_performance
        )

        st.pyplot(fig, width="stretch")

    elif option == "Product Profit Margin":

        fig = visualization_product_profit_margin(
            product_performance
        )

        st.pyplot(fig, width="stretch")

    elif option == "Revenue vs Profit":

        fig = visualization_revenue_vs_profit(
            product_performance
        )

        st.pyplot(fig, width="stretch")

    # =========================================================
    # PARTICULAR PRODUCT MONTHLY TREND
    # =========================================================

    st.divider()

    st.subheader("Monthly Product Revenue Trend")

    product_name = st.text_input(
        "Enter Product Name"
    )

    if product_name:

        try:

            monthly_product_data = get_monthly_product_trend(
                product_name
            )

            if monthly_product_data:

                fig = visualization_monthly_product_trend(
                    monthly_product_data
                )

                st.pyplot(fig, width="stretch")

            else:

                st.info(
                    "No data found for this product."
                )

        except Exception as e:

            st.error(
                "Could not retrieve product trend."
            )

            st.exception(e)

    # =========================================================
    # AI ANALYTICS ASSISTANT
    # =========================================================

    analytics_chat("product")