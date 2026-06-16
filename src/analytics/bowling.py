import pandas as pd

# Top wicket takers
def top_wicket_takers(deliveries, top_n = 10):

    wickets = deliveries[deliveries["player_dismissed"].notna()
    ]

    wickets = (
        wickets
        .groupby("bowler")
        .size()
        .reset_index(name="wickets")
        .sort_values(
            "wickets",
            ascending = False
        )
        .head(top_n)
    )
    return (
    wickets
    .sort_values("wickets", ascending=False)
    .head(top_n)
    .reset_index(drop=True)
)

# Top economy rate
def economy_rate(deliveries, top_n=10):

    legal_balls = deliveries[
        deliveries["isWide"] != 1
    ]

    balls = (
        legal_balls
        .groupby("bowler")
        .size()
        .reset_index(name="balls")
    )

    runs = (
        deliveries
        .groupby("bowler")
        .agg({
            "batsman_runs": "sum",
            "extras": "sum"
        })
        .reset_index()
    )

    runs["runs_conceded"] = (
        runs["batsman_runs"]
        + runs["extras"]
    )

    eco = runs.merge(
        balls,
        on="bowler"
    )

    eco["overs"] = eco["balls"] / 6

    eco["economy"] = (
        eco["runs_conceded"]
        / eco["overs"]
    )

    eco = eco[
        eco["balls"] >= 500
    ]

    return (
        eco.sort_values(
            "economy"
        )
        .head(top_n)
    )
    