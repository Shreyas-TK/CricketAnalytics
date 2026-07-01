"""Shared test configuration and fixtures."""
import pytest


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    from pathlib import Path
    return Path(__file__).parent.parent
