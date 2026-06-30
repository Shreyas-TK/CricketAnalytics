from typing import Any

import pandas as pd


def _legal_batting_deliveries(deliveries: pd.DataFrame) -> pd.DataFrame:
    """Return deliveries that count as balls faced by batters."""
    return deliveries[deliveries["isWide"] != 1]


def _player_deliveries(deliveries: pd.DataFrame, player: str) -> pd.DataFrame:
    """Return all deliveries faced by a batter."""
    return deliveries[deliveries["batsman"] == player]


def top_run_scorers(deliveries: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Return the top IPL run scorers."""
    return (
        deliveries.groupby("batsman", as_index=False)["batsman_runs"]
        .sum()
        .sort_values("batsman_runs", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def strike_rate(deliveries: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Return batters with the highest strike rate after a 500-ball cutoff."""
    balls = (
        _legal_batting_deliveries(deliveries)
        .groupby("batsman")
        .size()
        .rename("balls")
    )
    runs = deliveries.groupby("batsman")["batsman_runs"].sum()

    strike_rates = pd.concat([runs, balls], axis=1).dropna(subset=["balls"])
    strike_rates = strike_rates[strike_rates["balls"] >= 500].copy()
    strike_rates["strike_rate"] = (
        strike_rates["batsman_runs"] / strike_rates["balls"] * 100
    )

    return (
        strike_rates.reset_index()
        .sort_values("strike_rate", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def batting_average(deliveries: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Return batters with the highest average after a 1,000-run cutoff."""
    runs = deliveries.groupby("batsman")["batsman_runs"].sum()
    dismissals = (
        deliveries.loc[deliveries["player_dismissed"].notna(), "player_dismissed"]
        .value_counts()
        .rename("outs")
    )

    averages = pd.concat([runs, dismissals], axis=1).fillna({"outs": 0})
    averages = averages[
        (averages["outs"] > 0) & (averages["batsman_runs"] >= 1000)
    ].copy()
    averages["average"] = averages["batsman_runs"] / averages["outs"]

    return (
        averages.reset_index(names="batsman")
        .sort_values("average", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def boundary_percentage(
    deliveries: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return batters with the highest boundary-ball percentage."""
    balls = (
        _legal_batting_deliveries(deliveries)
        .groupby("batsman")
        .size()
        .rename("balls")
    )
    boundaries = (
        deliveries[deliveries["batsman_runs"].isin([4, 6])]
        .groupby("batsman")
        .size()
        .rename("boundaries")
    )

    result = pd.concat([balls, boundaries], axis=1).fillna({"boundaries": 0})
    result = result[result["balls"] >= 500].copy()
    result["boundary_pct"] = result["boundaries"] / result["balls"] * 100

    return (
        result.reset_index()
        .sort_values("boundary_pct", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def player_batting_summary(
    deliveries: pd.DataFrame,
    player: str,
) -> dict[str, Any]:
    """Return a batting summary for a single player."""
    player_df = _player_deliveries(deliveries, player)
    legal_balls = player_df[player_df["isWide"] != 1]

    runs = int(player_df["batsman_runs"].sum())
    balls_faced = int(len(legal_balls))
    outs = int((player_df["player_dismissed"] == player).sum())
    fours = int((player_df["batsman_runs"] == 4).sum())
    sixes = int((player_df["batsman_runs"] == 6).sum())

    strike_rate_value = runs / balls_faced * 100 if balls_faced else 0
    average = runs / outs if outs else runs
    boundary_pct = (fours + sixes) / balls_faced * 100 if balls_faced else 0

    return {
        "Runs": runs,
        "Matches": int(player_df["matchId"].nunique()),
        "Balls": balls_faced,
        "Average": round(average, 2),
        "Strike Rate": round(strike_rate_value, 2),
        "Fours": fours,
        "Sixes": sixes,
        "Boundary %": round(boundary_pct, 2),
        "Outs": outs,
    }


def player_runs_by_season(
    deliveries: pd.DataFrame,
    matches: pd.DataFrame,
    player: str,
) -> pd.DataFrame:
    """Return a player's total runs by IPL season."""
    player_df = _player_deliveries(deliveries, player).merge(
        matches[["matchId", "season"]],
        on="matchId",
        how="left",
    )

    return (
        player_df.groupby("season", as_index=False)["batsman_runs"]
        .sum()
        .sort_values("season")
        .reset_index(drop=True)
    )


def player_runs_against_teams(
    deliveries: pd.DataFrame,
    player: str,
) -> pd.DataFrame:
    """Return a player's runs grouped by bowling team."""
    player_df = _player_deliveries(deliveries, player)
    return (
        player_df.groupby("bowling_team", as_index=False)["batsman_runs"]
        .sum()
        .sort_values("batsman_runs", ascending=False)
        .reset_index(drop=True)
    )


def player_runs_by_venue(
    deliveries: pd.DataFrame,
    matches: pd.DataFrame,
    player: str,
) -> pd.DataFrame:
    """Return a player's runs grouped by venue."""
    player_df = _player_deliveries(deliveries, player).merge(
        matches[["matchId", "venue"]],
        on="matchId",
        how="left",
    )
    return (
        player_df.groupby("venue", as_index=False)["batsman_runs"]
        .sum()
        .sort_values("batsman_runs", ascending=False)
        .reset_index(drop=True)
    )


def player_dismissal_types(
    deliveries: pd.DataFrame,
    player: str,
) -> pd.DataFrame:
    """Return dismissal counts by dismissal type for one batter."""
    dismissals = deliveries[deliveries["player_dismissed"] == player]
    return (
        dismissals.groupby("dismissal_kind")
        .size()
        .reset_index(name="dismissals")
        .sort_values("dismissals", ascending=False)
        .reset_index(drop=True)
    )


def player_scoring_distribution(
    deliveries: pd.DataFrame,
    player: str,
) -> pd.DataFrame:
    """Return frequency of runs scored per delivery by one batter."""
    score_dist = (
        _player_deliveries(deliveries, player)["batsman_runs"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    score_dist.columns = ["Runs Scored", "Frequency"]
    return score_dist


def player_highest_score(deliveries: pd.DataFrame, player: str) -> int:
    """Return a player's highest score in an IPL match."""
    innings = _player_deliveries(deliveries, player).groupby("matchId")[
        "batsman_runs"
    ]
    highest = innings.sum().max()
    return int(highest) if pd.notna(highest) else 0


def player_milestones(
    deliveries: pd.DataFrame,
    player: str,
) -> dict[str, int]:
    """Return counts of 50s and 100s for one batter."""
    innings = (
        _player_deliveries(deliveries, player)
        .groupby("matchId")["batsman_runs"]
        .sum()
    )

    return {
        "50s": int(((innings >= 50) & (innings < 100)).sum()),
        "100s": int((innings >= 100).sum()),
    }
