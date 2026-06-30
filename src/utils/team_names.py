from typing import Final

import pandas as pd

TEAM_MAPPING: Final[dict[str, str]] = {
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Kings XI Punjab": "Punjab Kings",
    "Delhi Daredevils": "Delhi Capitals",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Pune Warriors": "Rising Pune Supergiant",
}


def standardize_team_names(matches: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of match data with legacy IPL team names normalized."""
    matches = matches.copy()

    for col in ("team1", "team2", "winner", "toss_winner"):
        if col not in matches.columns:
            continue
        matches[col] = matches[col].replace(TEAM_MAPPING)

    return matches
