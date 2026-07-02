from __future__ import annotations

from typing import Any

import pandas as pd


REQUIRED_MATCH_COLUMNS = {
    "matchId",
    "season",
    "date",
    "team1",
    "team2",
    "venue",
    "toss_winner",
    "toss_decision",
    "winner",
}

REQUIRED_DELIVERY_COLUMNS = {
    "matchId",
    "inning",
    "over",
    "ball",
    "batsman",
    "bowler",
    "batsman_runs",
    "isWide",
    "player_dismissed",
    "dismissal_kind",
    "bowling_team",
}


def validate_ipl_data(matches: pd.DataFrame, deliveries: pd.DataFrame) -> dict[str, Any]:
    """Validate the IPL match and delivery datasets and return a summary report."""
    missing_matches = sorted(REQUIRED_MATCH_COLUMNS - set(matches.columns))
    missing_deliveries = sorted(REQUIRED_DELIVERY_COLUMNS - set(deliveries.columns))

    issues: list[str] = []
    if missing_matches:
        issues.append(f"Missing match columns: {', '.join(missing_matches)}")
    if missing_deliveries:
        issues.append(f"Missing delivery columns: {', '.join(missing_deliveries)}")

    match_missing = matches.isna().sum().to_dict()
    delivery_missing = deliveries.isna().sum().to_dict()
    summary = {
        "status": "pass" if not issues else "warn",
        "matches_rows": int(len(matches)),
        "deliveries_rows": int(len(deliveries)),
        "required_columns": {
            "matches": sorted(REQUIRED_MATCH_COLUMNS),
            "deliveries": sorted(REQUIRED_DELIVERY_COLUMNS),
        },
        "missing_values": {
            "matches": match_missing,
            "deliveries": delivery_missing,
        },
        "issues": issues,
    }
    return summary
