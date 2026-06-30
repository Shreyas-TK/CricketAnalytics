import matplotlib.pyplot as plt
import pandas as pd


def plot_top_wicket_takers(df: pd.DataFrame) -> None:
    """Save and display a matplotlib bar chart of top wicket takers."""
    sorted_df = df.sort_values("wickets", ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(
        sorted_df["bowler"],
        sorted_df["wickets"],
    )
    plt.xlabel("Wickets")
    plt.ylabel("Bowler")
    plt.title("Top IPL Wicket Takers")
    plt.tight_layout()
    plt.savefig("reports/figures/top_wicket_takers.png")
    plt.show()
