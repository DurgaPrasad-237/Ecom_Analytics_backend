import streamlit as st

from views.customer import customer_page
from views.products import product_page


st.set_page_config(
    page_title="Indian E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)


st.title("Indian E-Commerce Analytics Platform")


selected_tab = st.sidebar.radio(
    "Select a section",
    [
        "Customer",
        "Products",
        "Shipments",
        "Payments",
        "Ratings",
        "Order Items"
    ]
)


if selected_tab == "Customer":

    customer_page()


elif selected_tab == "Products":

    product_page()


elif selected_tab == "Shipments":

    st.title("Shipments Analytics")
    st.info("Shipments analytics coming soon.")


elif selected_tab == "Payments":

    st.title("Payments Analytics")
    st.info("Payments analytics coming soon.")


elif selected_tab == "Ratings":

    st.title("Ratings Analytics")
    st.info("Ratings analytics coming soon.")


elif selected_tab == "Order Items":

    st.title("Order Items Analytics")
    st.info("Order Items analytics coming soon.")