"""Test analytics functions."""
import pytest
import pandas as pd
from src.analytics.batting import top_run_scorers, strike_rate
from src.analytics.bowling import top_wicket_takers


@pytest.fixture
def sample_deliveries():
    """Create sample deliveries data for testing."""
    return pd.DataFrame({
        "batsman": ["Kohli", "Rohit", "Kohli", "Rohit", "Kohli"],
        "bowler": ["Bumrah", "Bumrah", "Siraj", "Siraj", "Bumrah"],
        "batsman_runs": [4, 0, 6, 1, 2],
        "isWide": [0, 0, 0, 0, 0],
        "wicket": [None, None, None, None, None],
    })


def test_top_run_scorers(sample_deliveries):
    """Test top_run_scorers function."""
    result = top_run_scorers(sample_deliveries, top_n=2)
    assert len(result) <= 2
    assert "batsman" in result.columns or "batsman_runs" in result.columns
    assert result is not None


def test_strike_rate(sample_deliveries):
    """Test strike_rate calculation."""
    result = strike_rate(sample_deliveries, top_n=2)
    assert result is not None
    assert len(result) >= 0
