from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def build_processed_datasets(
    matches: pd.DataFrame,
    deliveries: pd.DataFrame,
    output_dir: str | Path | None = None,
) -> tuple[Path, Path]:
    """Create reproducible processed datasets from the raw IPL data."""
    base_dir = Path(output_dir) if output_dir is not None else Path(__file__).resolve().parents[2] / "data" / "processed"
    base_dir.mkdir(parents=True, exist_ok=True)

    matches_out = base_dir / "matches_processed.csv"
    deliveries_out = base_dir / "deliveries_processed.csv"

    cleaned_matches = matches.copy()
    cleaned_deliveries = deliveries.copy()

    cleaned_matches["date"] = pd.to_datetime(cleaned_matches["date"], errors="coerce")
    cleaned_deliveries["batsman_runs"] = pd.to_numeric(cleaned_deliveries["batsman_runs"], errors="coerce")
    cleaned_deliveries["isWide"] = pd.to_numeric(cleaned_deliveries["isWide"], errors="coerce")

    cleaned_matches.to_csv(matches_out, index=False)
    cleaned_deliveries.to_csv(deliveries_out, index=False)
    return matches_out, deliveries_out
