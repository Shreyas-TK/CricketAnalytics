import pandas as pd

def load_data():
    matches = pd.read_csv("/Users/shreyastk/CricketAnalytics/data/raw/matches_updated_ipl_upto_2025.csv")

    deliveries = pd.read_csv("/Users/shreyastk/CricketAnalytics/data/raw/deliveries_updated_ipl_upto_2025.csv")

    return matches, deliveries
    