import pandas as pd

# Top run scorers 
def top_runs_scorers(deliveries, top_n = 10):
    runs = (
        deliveries
        .groupby("batsman")["batsman_runs"]
        .sum()
        .reset_index()
        .sort_values(
            by = ["batsman_runs"],
            ascending = False 
        ).head(top_n)
    )
    return runs

# StrikeRate calculation 
def strike_rate(deliveries, top_n = 10):
    #Total balls
    balls = (
        deliveries
        .groupby("batsman")
        .size()
        .reset_index(name="balls")
    )
    #Total runs 
    runs = (
        deliveries
        .groupby("batsman")["batsman_runs"]
        .sum()
        .reset_index()
     )
    #Strikerate calculation 
    sr = runs.merge(balls,on="batsman")

    sr["strike_rate"] = (
        sr['batsman_runs'] / sr["balls"] * 100
     )

    sr = sr[
        sr["balls"] >= 500
    ]

    return sr.sort_values(
        by="strike_rate",
        ascending=False
    ).head(top_n)