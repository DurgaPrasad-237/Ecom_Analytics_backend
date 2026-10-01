import pandas as pd

def load_order_items_data(path):
    order_items = pd.read_csv(path)
    return order_items