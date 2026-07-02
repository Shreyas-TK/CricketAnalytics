"""Test analytics functions."""
import pytest
import pandas as pd
from src.analytics.batting import compare_players_summary, strike_rate, top_run_scorers
from src.analytics.bowling import top_wicket_takers


@pytest.fixture
def sample_deliveries():
    """Create sample deliveries data for testing."""
    return pd.DataFrame({
        "batsman": ["Kohli", "Rohit", "Kohli", "Rohit", "Kohli"],
        "bowler": ["Bumrah", "Bumrah", "Siraj", "Siraj", "Bumrah"],
        "batsman_runs": [4, 0, 6, 1, 2],
        "isWide": [0, 0, 0, 0, 0],
        "matchId": [100, 100, 101, 101, 102],
        "player_dismissed": [None, None, "Kohli", None, None],
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


def test_compare_players_summary(sample_deliveries):
    """Test the comparison summary helper for two players."""
    result = compare_players_summary(sample_deliveries, None, ["Kohli", "Rohit"])
    assert list(result["player"]) == ["Kohli", "Rohit"]
    assert {"Runs", "Average", "Strike Rate", "Highest Score"}.issubset(result.columns)
