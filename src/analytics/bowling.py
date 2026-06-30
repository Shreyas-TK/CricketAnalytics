from typing import Any

import pandas as pd


def _bowler_deliveries(deliveries: pd.DataFrame, bowler: str) -> pd.DataFrame:
    """Return all deliveries bowled by one player."""
    return deliveries[deliveries["bowler"] == bowler]


def _wicket_deliveries(deliveries: pd.DataFrame) -> pd.DataFrame:
    """Return rows where a wicket fell."""
    return deliveries[deliveries["player_dismissed"].notna()]


def _legal_bowling_deliveries(deliveries: pd.DataFrame) -> pd.DataFrame:
    """Return deliveries that count toward a bowler's over."""
    return deliveries[deliveries["isWide"] != 1]


def top_wicket_takers(
    deliveries: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return the top IPL wicket takers."""
    return (
        _wicket_deliveries(deliveries)
        .groupby("bowler")
        .size()
        .reset_index(name="wickets")
        .sort_values("wickets", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def economy_rate(deliveries: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Return bowlers with the best economy after a 500-ball cutoff."""
    balls = (
        _legal_bowling_deliveries(deliveries)
        .groupby("bowler")
        .size()
        .rename("balls")
    )
    runs = deliveries.groupby("bowler")[["batsman_runs", "extras"]].sum()
    economy = pd.concat([runs, balls], axis=1).dropna(subset=["balls"])
    economy = economy[economy["balls"] >= 500].copy()
    economy["runs_conceded"] = economy["batsman_runs"] + economy["extras"]
    economy["overs"] = economy["balls"] / 6
    economy["economy"] = economy["runs_conceded"] / economy["overs"]

    return (
        economy.reset_index()
        .sort_values("economy")
        .head(top_n)
        .reset_index(drop=True)
    )


def bowler_summary(deliveries: pd.DataFrame, bowler: str) -> dict[str, Any]:
    """Return a bowling summary for one bowler."""
    bowler_df = _bowler_deliveries(deliveries, bowler)
    legal_balls = _legal_bowling_deliveries(bowler_df)

    wickets = int(bowler_df["player_dismissed"].notna().sum())
    balls = int(len(legal_balls))
    runs = int(bowler_df["batsman_runs"].sum() + bowler_df["extras"].sum())
    overs = round(balls / 6, 1)
    economy = runs / (balls / 6) if balls else 0
    average = runs / wickets if wickets else 0
    strike_rate_value = balls / wickets if wickets else 0

    return {
        "Matches": int(bowler_df["matchId"].nunique()),
        "Wickets": wickets,
        "Overs": overs,
        "Runs": runs,
        "Economy": round(economy, 2),
        "Average": round(average, 2),
        "Strike Rate": round(strike_rate_value, 2),
    }


def wickets_by_season(
    deliveries: pd.DataFrame,
    matches: pd.DataFrame,
    bowler: str,
) -> pd.DataFrame:
    """Return a bowler's wickets by IPL season."""
    bowler_df = _bowler_deliveries(deliveries, bowler).merge(
        matches[["matchId", "season"]],
        on="matchId",
        how="left",
    )

    return (
        _wicket_deliveries(bowler_df)
        .groupby("season")
        .size()
        .reset_index(name="wickets")
        .sort_values("season")
        .reset_index(drop=True)
    )


def wickets_against_teams(
    deliveries: pd.DataFrame,
    bowler: str,
) -> pd.DataFrame:
    """Return a bowler's wickets grouped by batting team."""
    return (
        _wicket_deliveries(_bowler_deliveries(deliveries, bowler))
        .groupby("batting_team")
        .size()
        .reset_index(name="wickets")
        .sort_values("wickets", ascending=False)
        .reset_index(drop=True)
    )


def wickets_by_venue(
    deliveries: pd.DataFrame,
    matches: pd.DataFrame,
    bowler: str,
) -> pd.DataFrame:
    """Return a bowler's wickets grouped by venue."""
    bowler_df = _bowler_deliveries(deliveries, bowler).merge(
        matches[["matchId", "venue"]],
        on="matchId",
        how="left",
    )

    return (
        _wicket_deliveries(bowler_df)
        .groupby("venue")
        .size()
        .reset_index(name="wickets")
        .sort_values("wickets", ascending=False)
        .reset_index(drop=True)
    )


def best_bowling_figures(deliveries: pd.DataFrame, bowler: str) -> int:
    """Return the maximum wickets taken by a bowler in one match."""
    wickets_by_match = (
        _wicket_deliveries(_bowler_deliveries(deliveries, bowler))
        .groupby("matchId")
        .size()
    )
    best = wickets_by_match.max()
    return int(best) if pd.notna(best) else 0


def bowling_milestones(
    deliveries: pd.DataFrame,
    bowler: str,
) -> dict[str, int]:
    """Return counts of 3-wicket and 5-wicket hauls for one bowler."""
    wickets_by_match = (
        _wicket_deliveries(_bowler_deliveries(deliveries, bowler))
        .groupby("matchId")
        .size()
    )

    return {
        "3W": int(((wickets_by_match >= 3) & (wickets_by_match < 5)).sum()),
        "5W": int((wickets_by_match >= 5).sum()),
    }


def wiickets_by_season(
    deliveries: pd.DataFrame,
    matches: pd.DataFrame,
    bowler: str,
) -> pd.DataFrame:
    """Backward-compatible alias for the misspelled legacy function name."""
    return wickets_by_season(deliveries, matches, bowler)


def wicket_againt_teams(deliveries: pd.DataFrame, bowler: str) -> pd.DataFrame:
    """Backward-compatible alias for the misspelled legacy function name."""
    return wickets_against_teams(deliveries, bowler)
