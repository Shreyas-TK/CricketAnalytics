import matplotlib.pyplot as plt
import pandas as pd


def plot_team_win_percentage(df: pd.DataFrame) -> None:
    """Display a matplotlib bar chart of the top team win percentages."""
    top_teams = df.head(10)

    plt.figure(figsize=(12, 6))
    plt.bar(
        top_teams["team"],
        top_teams["win_pct"],
    )
    plt.xticks(rotation=45)
    plt.ylabel("Win Percentage")
    plt.title("IPL Team Win Percentage")
    plt.tight_layout()
    plt.show()
