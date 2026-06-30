import matplotlib.pyplot as plt
import pandas as pd


def plot_top_run_scorers(df: pd.DataFrame) -> None:
    """Save and display a matplotlib bar chart of top run scorers."""
    sorted_df = df.sort_values("batsman_runs", ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(
        sorted_df["batsman"],
        sorted_df["batsman_runs"],
    )
    plt.xlabel("Runs")
    plt.ylabel("Batsman")
    plt.title("Top IPL Run Scorers")
    plt.tight_layout()
    plt.savefig("reports/figures/top_run_scorers.png")
    plt.show()
