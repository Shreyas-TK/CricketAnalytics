"""Tests for the data quality validation layer."""

import pytest

from src.data_loader import load_data
from src.services.data_quality import validate_ipl_data


def test_validate_ipl_data_reports_quality_summary():
    try:
        matches, deliveries = load_data()
    except FileNotFoundError:
        pytest.skip("Required IPL data files are not present")

    report = validate_ipl_data(matches, deliveries)

    assert report["status"] in {"pass", "warn"}
    assert report["matches_rows"] >= 1
    assert report["deliveries_rows"] >= 1
    assert "missing_values" in report
    assert "required_columns" in report
    assert "issues" in report
