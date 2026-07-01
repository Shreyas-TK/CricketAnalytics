"""Test the ML model persistence layer."""

import pytest
from src.ml.predictive_model import get_match_outcome_model
from src.data_loader import load_data


def test_ml_model_persistence():
    try:
        matches, _ = load_data()
    except FileNotFoundError:
        pytest.skip("Data files not present for ML model persistence test")

    model, status = get_match_outcome_model(matches)
    assert model is not None
    assert isinstance(status, str)
    assert status == "Saved model loaded" or status.endswith("%")
