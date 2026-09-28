import streamlit as st

from app.api_client import (
    get_monthly_signups,
    get_monthly_signups_gender,
    get_signup_trend,
    get_customer_churn,
    get_total_customers,
    get_churned_rate,
    get_avg_customer_spend,
    get_avg_order_value,
    get_customer_segment,
    
)

from analytics.customer_analytics.visualization import (
    visualization_monthly_signup,
    visualization_monthly_signup_gender,
    visualization_signup_trend_yearwise,
    visualization_churn,
    visualization_customer_segment,
    Visualization_total_spending_by_customer_segment,
    Visualization_Average_Spend_by_Customer_Segment,
    Visualization_avg_vs_median_spend,
    Visualization_coeff_of_variation_by_segment,
    Visualization_customer_count_by_segment,
    Visualization_spend_distirubtion_by_segment
)
from components.chat import analytics_chat
from api.main import df



def customer_page():
    
    st.title("Customer Analytics")

    st.caption(
        "Analyze customer acquisition, churn, spending, and segments."
    )

    # -----------------------------
    # Get data from FastAPI
    # -----------------------------

    try:

        monthly_signups = get_monthly_signups()

        monthly_signups_gender = get_monthly_signups_gender()

        signup_trend = get_signup_trend()

        customer_churn = get_customer_churn()

        customer_segment = get_customer_segment()

        customer_segment1 = get_customer_segment()

    except Exception as e:

        st.error(
            "Could not connect to FastAPI. "
            "Make sure FastAPI is running on port 8000."
        )

        st.exception(e)

        return

    # -----------------------------
    # KPI cards
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Customers",
        get_total_customers()['total_customers']
    )

    col2.metric(
        "Churn Rate",
        f"{round(get_churned_rate()['churn_rate'], 3)} %"
    )

    col3.metric(
        "Average Customer Spend",
        f"₹{get_avg_customer_spend()['average_customer_spend']:,.0f}"
    )

    col4.metric(
        "Average Order Value",
        f"{get_avg_order_value()['average_order_value']:,.2f}"
    )

    st.divider()

    # -----------------------------
    # Monthly Signups
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Monthly Customer Signups")

        fig = visualization_monthly_signup(
            monthly_signups
        )

        st.pyplot(fig, width="stretch")

    # -----------------------------
    # Signup by Gender
    # -----------------------------

    with col2:

        st.subheader("Customer Signups by Gender")

        fig = visualization_monthly_signup_gender(
            monthly_signups_gender
        )

        st.pyplot(fig, width="stretch")

    # -----------------------------
    # Year-wise Trend
    # -----------------------------

    st.subheader("Year-wise Customer Signup Trend")

    fig = visualization_signup_trend_yearwise(
        signup_trend
    )

    st.pyplot(fig, width="stretch")

    # -----------------------------
    # Customer Churn
    # -----------------------------
    
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Customer Status")

        fig = visualization_churn(
            customer_churn
        )

        st.pyplot(fig, width="stretch")

    with col2:
        dropdown_col, _ = st.columns([1, 1])

        with dropdown_col:
            option = st.selectbox(
                "Customer Segment Analysis",
                (
                    "Average Spend by Customer Segment",
                    "Total Spending by Customer Segment",
                    "Customer Count by Segment",
                    "Average vs Median Spend",
                    "Spending Distribution by Segment",
                    "Coefficient of Variation by Segment"
                )
            )
       
        if option == "Average Spend by Customer Segment":
            fig = Visualization_Average_Spend_by_Customer_Segment(customer_segment1)
            st.pyplot(fig, width="stretch")

        elif option == "Total Spending by Customer Segment":
            fig = Visualization_total_spending_by_customer_segment(customer_segment1)
            st.pyplot(fig, width="stretch")

        elif option == "Customer Count by Segment":
            fig = Visualization_customer_count_by_segment(customer_segment1)
            st.pyplot(fig, width="stretch")

        elif option == "Average vs Median Spend":
            fig = Visualization_avg_vs_median_spend(customer_segment1)
            st.pyplot(fig, width="stretch")

        elif option == "Spending Distribution by Segment":
            fig = Visualization_spend_distirubtion_by_segment(df)
            st.pyplot(fig, width="stretch")

        elif option == "Coefficient of Variation by Segment":
            fig = Visualization_coeff_of_variation_by_segment(customer_segment1)
            st.pyplot(fig, width="stretch")
        else:
            st.info("soon")

            
        
        

    # -----------------------------
    # AI Analytics Assistant
    # -----------------------------
    
    analytics_chat("customer")