import pandas as pd

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