import pandas as pd

def standardize_column_names():
    pass

def clean_string_values(
     df_customer,
     df_customer_review,
     df_orders,
     df_order_items,
     df_products,
     df_payments,
     df_returns,
     df_shipments
):
    # ============ customers ==================
    df_customer["gender"] = df_customer['gender'].str.strip().str.lower()
    df_customer["state"] = df_customer['state'].str.strip().str.lower()
    df_customer["city"] = df_customer['city'].str.strip().str.lower()
    df_customer["customer_segment"] = df_customer['customer_segment'].str.strip().str.lower()
    df_customer["preferred_device"] = df_customer['preferred_device'].str.strip().str.lower()
    df_customer["preferred_payment_method"] = df_customer['preferred_payment_method'].str.strip().str.lower()
    df_customer["acquisition_channel"] = df_customer['acquisition_channel'].str.strip().str.lower()
    df_customer["loyalty_tier"] = df_customer['loyalty_tier'].str.strip().str.lower()
    df_customer["customer_status"] = df_customer['customer_status'].str.strip().str.lower()

    # ============= customer reviews ===================
    df_customer_review['review_sentiment'] = df_customer_review['review_sentiment'].str.strip().str.lower()

    # ================ orders ===========================
    df_orders_cat_col = df_orders.select_dtypes(include="object").columns
    for i in df_orders_cat_col:
        df_orders[i] = df_orders[i].str.strip().str.lower()  

    # ========== order_items =========================
    df_order_items_cal_col = df_order_items.select_dtypes(include="object").columns
    for i in df_order_items_cal_col:
        df_order_items[i] = df_order_items[i].str.strip().str.lower()

    # =============== products =========================
    df_products_cat_col = df_products.select_dtypes(include="object").columns
    for i in df_products_cat_col:
        df_products[i] = df_products[i].str.strip().str.lower()

    # =============== payments ============================
    df_payments_cat_col = df_payments.select_dtypes(include="object").columns
    for i in df_payments_cat_col:
        df_payments[i] = df_payments[i].str.strip().str.lower()

    # =============== returns ===============================
    df_returns_cat_col = df_returns.select_dtypes(include="object").columns
    for i in df_returns_cat_col:
         df_returns[i] = df_returns[i].str.strip().str.lower()


    # =================== shipments ===========================
    df_shipments_cat_col = df_shipments.select_dtypes(include="object").columns
    for i in df_shipments_cat_col:
        df_shipments[i] = df_shipments[i].str.strip().str.lower()
