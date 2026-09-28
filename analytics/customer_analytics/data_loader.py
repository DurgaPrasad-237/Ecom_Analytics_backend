import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_customer_data(path):
    df = pd.read_csv(path)
    return df


