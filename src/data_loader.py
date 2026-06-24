import pandas as pd
from src.utils.team_names import standardize_team_names

def load_data():
    matches = pd.read_csv("/Users/shreyastk/CricketAnalytics/data/raw/matches_updated_ipl_upto_2025.csv")
    matches = standardize_team_names(matches)

    deliveries = pd.read_csv("/Users/shreyastk/CricketAnalytics/data/raw/deliveries_updated_ipl_upto_2025.csv")

    return matches, deliveries
