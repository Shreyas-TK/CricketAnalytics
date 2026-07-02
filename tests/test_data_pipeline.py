"""Tests for the reproducible data pipeline."""

import pandas as pd
import pytest

from src.data_loader import load_data
from src.services.data_pipeline import build_processed_datasets


def test_build_processed_datasets_creates_outputs(tmp_path):
    try:
        matches, deliveries = load_data()
    except FileNotFoundError:
        pytest.skip("Required IPL data files are not present")

    match_path, delivery_path = build_processed_datasets(
        matches,
        deliveries,
        output_dir=tmp_path,
    )

    assert match_path.exists()
    assert delivery_path.exists()
    assert len(pd.read_csv(match_path)) == len(matches)
    assert len(pd.read_csv(delivery_path)) == len(deliveries)
