"""Test data loading functionality."""
import pytest
from pathlib import Path
from src.data_loader import load_data


def test_load_data_returns_tuple():
    """Test that load_data returns a tuple of two DataFrames."""
    try:
        matches, deliveries = load_data()
        assert matches is not None
        assert deliveries is not None
        assert len(matches) > 0
        assert len(deliveries) > 0
    except FileNotFoundError:
        pytest.skip("Data files not found in expected location")


def test_load_data_matches_structure():
    """Test that matches DataFrame has expected columns."""
    try:
        matches, _ = load_data()
        assert "season" in matches.columns
        assert "team1" in matches.columns or "Team1" in matches.columns
        assert len(matches) > 0
    except FileNotFoundError:
        pytest.skip("Data files not found in expected location")


def test_load_data_deliveries_structure():
    """Test that deliveries DataFrame has expected columns."""
    try:
        _, deliveries = load_data()
        assert "batsman" in deliveries.columns or "batter" in deliveries.columns
        assert "bowler" in deliveries.columns
        assert len(deliveries) > 0
    except FileNotFoundError:
        pytest.skip("Data files not found in expected location")
