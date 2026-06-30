from pathlib import Path

import pandas as pd

from src.utils.team_names import standardize_team_names

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
MATCHES_FILE = RAW_DATA_DIR / "matches_updated_ipl_upto_2025.csv"
DELIVERIES_FILE = RAW_DATA_DIR / "deliveries_updated_ipl_upto_2025.csv"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load and lightly standardize IPL matches and delivery-level data."""
    if not MATCHES_FILE.exists() or not DELIVERIES_FILE.exists():
        missing = [
            str(path)
            for path in (MATCHES_FILE, DELIVERIES_FILE)
            if not path.exists()
        ]
        raise FileNotFoundError(
            "Required IPL data file(s) were not found: " + ", ".join(missing)
        )

    matches = standardize_team_names(pd.read_csv(MATCHES_FILE))
    deliveries = pd.read_csv(DELIVERIES_FILE)

    return matches, deliveries
