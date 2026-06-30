from typing import Any

import pandas as pd


def _matches_for_team(matches: pd.DataFrame, team: str) -> pd.DataFrame:
    """Return matches where the selected team played."""
    return matches[(matches["team1"] == team) | (matches["team2"] == team)]


def team_win_percentage(matches: pd.DataFrame) -> pd.DataFrame:
    """Return win percentage for teams with at least 100 matches played."""
    wins = matches["winner"].value_counts().rename("wins")
    matches_played = (
        matches["team1"]
        .value_counts()
        .add(matches["team2"].value_counts(), fill_value=0)
        .rename("matches_played")
    )

    result = pd.concat([matches_played, wins], axis=1).fillna({"wins": 0})
    result["win_pct"] = result["wins"] / result["matches_played"] * 100
    result = result[result["matches_played"] >= 100]

    return (
        result.reset_index(names="team")
        .sort_values("win_pct", ascending=False)
        .reset_index(drop=True)
    )


def toss_impact(matches: pd.DataFrame) -> float:
    """Return the percentage of completed matches won by the toss winner."""
    completed_matches = matches[matches["winner"].notna()]
    if completed_matches.empty:
        return 0.0

    toss_wins = (
        completed_matches["toss_winner"] == completed_matches["winner"]
    ).sum()
    return round(toss_wins / len(completed_matches) * 100, 2)


def highest_scoring_venues(
    matches: pd.DataFrame,
    deliveries: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return venues with the highest average innings score."""
    innings_scores = (
        deliveries.groupby(["matchId", "inning"], as_index=False)[
            ["batsman_runs", "extras"]
        ]
        .sum()
        .assign(
            total_score=lambda df: df["batsman_runs"] + df["extras"],
        )
    )

    venue_scores = (
        innings_scores.merge(matches[["matchId", "venue"]], on="matchId")
        .groupby("venue", as_index=False)
        .agg(
            avg_score=("total_score", "mean"),
            innings_count=("total_score", "count"),
        )
    )
    venue_scores = venue_scores[venue_scores["innings_count"] >= 20].copy()
    venue_scores["avg_score"] = venue_scores["avg_score"].round(2)

    return (
        venue_scores.sort_values("avg_score", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def venue_toss_impact(
    matches: pd.DataFrame,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return venues where toss winners most often also win the match."""
    venue_stats = (
        matches.assign(toss_match_win=matches["toss_winner"] == matches["winner"])
        .groupby("venue", as_index=False)
        .agg(
            matches=("matchId", "count"),
            toss_match_win_pct=("toss_match_win", "mean"),
        )
    )
    venue_stats["toss_match_win_pct"] = (
        venue_stats["toss_match_win_pct"] * 100
    ).round(2)
    venue_stats = venue_stats[venue_stats["matches"] >= 10]

    return (
        venue_stats.sort_values("toss_match_win_pct", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def team_summary(
    matches: pd.DataFrame,
    deliveries: pd.DataFrame,
    team: str,
) -> dict[str, Any]:
    """Return match-level summary metrics for one IPL team."""
    team_matches = _matches_for_team(matches, team)
    played = len(team_matches)
    wins = int((team_matches["winner"] == team).sum())
    losses = played - wins
    win_pct = wins / played * 100 if played else 0
    toss_wins = int((team_matches["toss_winner"] == team).sum())

    return {
        "Matches": int(played),
        "Wins": wins,
        "Losses": int(losses),
        "Win %": round(win_pct, 2),
        "Toss Wins": toss_wins,
    }


def team_top_batter(
    deliveries: pd.DataFrame,
    team: str,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return top run scorers for one team."""
    return (
        deliveries[deliveries["batting_team"] == team]
        .groupby("batsman", as_index=False)["batsman_runs"]
        .sum()
        .sort_values("batsman_runs", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def team_top_bowler(
    deliveries: pd.DataFrame,
    team: str,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return top wicket takers for one team."""
    return (
        deliveries[
            (deliveries["bowling_team"] == team)
            & deliveries["player_dismissed"].notna()
        ]
        .groupby("bowler")
        .size()
        .reset_index(name="wickets")
        .sort_values("wickets", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def team_win_by_season(matches: pd.DataFrame, team: str) -> pd.DataFrame:
    """Return a team's win percentage by season."""
    season = (
        _matches_for_team(matches, team)
        .assign(is_win=lambda df: df["winner"] == team)
        .groupby("season", as_index=False)
        .agg(matches=("matchId", "count"), wins=("is_win", "sum"))
    )
    season["win_pct"] = season["wins"] / season["matches"] * 100
    return season.sort_values("season").reset_index(drop=True)


def venue_summary(
    matches: pd.DataFrame,
    deliveries: pd.DataFrame,
    venue: str,
) -> dict[str, Any]:
    """Return summary metrics for one IPL venue."""
    venue_matches = matches[matches["venue"] == venue]
    venue_deliveries = deliveries[
        deliveries["matchId"].isin(venue_matches["matchId"])
    ]

    innings_scores = (
        venue_deliveries.groupby(["matchId", "inning"])[["batsman_runs", "extras"]]
        .sum()
        .sum(axis=1)
    )

    return {
        "Matches": int(len(venue_matches)),
        "Avg Innings Score": round(float(innings_scores.mean()), 2)
        if not innings_scores.empty
        else 0,
        "Highest Innings Score": int(innings_scores.max())
        if not innings_scores.empty
        else 0,
        "Toss Win Match Win %": round(
            float(
                (
                    venue_matches["toss_winner"] == venue_matches["winner"]
                ).mean()
                * 100
            ),
            2,
        )
        if not venue_matches.empty
        else 0,
    }


def venue_runs_by_season(
    matches: pd.DataFrame,
    deliveries: pd.DataFrame,
    venue: str,
) -> pd.DataFrame:
    """Return average innings score by season for one venue."""
    venue_matches = matches.loc[
        matches["venue"] == venue,
        ["matchId", "season"],
    ]
    if venue_matches.empty:
        return pd.DataFrame(columns=["season", "avg_score"])

    innings_scores = (
        deliveries.merge(venue_matches, on="matchId")
        .groupby(["season", "matchId", "inning"], as_index=False)[
            ["batsman_runs", "extras"]
        ]
        .sum()
        .assign(total_score=lambda df: df["batsman_runs"] + df["extras"])
    )

    return (
        innings_scores.groupby("season", as_index=False)["total_score"]
        .mean()
        .rename(columns={"total_score": "avg_score"})
        .sort_values("season")
        .reset_index(drop=True)
    )


def venue_team_wins(
    matches: pd.DataFrame,
    venue: str,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return teams with the most wins at one venue."""
    return (
        matches[(matches["venue"] == venue) & matches["winner"].notna()]
        .groupby("winner")
        .size()
        .reset_index(name="wins")
        .sort_values("wins", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
