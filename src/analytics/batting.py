import pandas as pd

# Top run scorers 
def top_run_scorers(deliveries, top_n = 10):
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

    legal_balls = deliveries[
        deliveries["isWide"] != 1
    ]
        
    #Total balls
    balls = (
        legal_balls
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

def batting_average(deliveries, top_n = 10):
    runs = (
        deliveries
        .groupby("batsman")["batsman_runs"]
        .sum()
        .reset_index()
     )

    dismissals = (
        deliveries[
            deliveries["player_dismissed"].notna()
        ]
        .groupby("player_dismissed")
        .size()
        .reset_index(name="outs")
     )

    dismissals.rename(
        columns={"player_dismissed":"batsman"},
        inplace = True
    )
    avg = runs.merge(
        dismissals,
        on="batsman",
        how="left"
    )

    avg["outs"] = avg["outs"].fillna(0)

    avg = avg[avg["outs"] > 0
    ]

    avg["average"] = (
        avg["batsman_runs"] / avg["outs"]
    )

    avg = avg[avg["batsman_runs"] >= 1000]

    return (
        avg.sort_values(
            "average",
            ascending=False
        ).head(top_n)
    )


