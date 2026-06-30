import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_data  # noqa: E402

PAGE_SUBTITLES = {
    "Overview": "A polished command center for IPL trends, records, and venue intelligence.",
    "Player Analytics": "Inspect batting form, scoring range, dismissals, venues, and opposition splits.",
    "Bowler Analytics": "Compare wicket trends, economy signals, matchups, venues, and haul milestones.",
    "Team Analytics": "Track team performance across seasons and identify top contributors.",
    "Venue Analytics": "Understand venue scoring behavior, toss outcomes, and home-ground leaders.",
}


def configure_page(title: str, icon: str) -> None:
    """Apply consistent Streamlit page configuration."""
    st.set_page_config(
        page_title=f"{title} | IPL Cricket Analytics",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_theme() -> None:
    """Deprecated theme hook kept for backward compatibility."""
    return None


@st.cache_data(show_spinner=False)
def get_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load IPL data once per Streamlit session."""
    return load_data()


def render_sidebar() -> None:
    """Render shared sidebar context without duplicating Streamlit navigation."""
    return None


def render_page_header(
    title: str,
    icon: str,
    subtitle: str | None = None,
    stats: dict[str, Any] | None = None,
) -> None:
    """Render a native Streamlit page header."""
    description = subtitle or PAGE_SUBTITLES.get(title, "")
    st.caption("IPL Cricket Analytics")
    st.title(f"{icon} {title}")
    if description:
        st.write(description)
    if stats:
        columns = st.columns(len(stats), gap="medium")
        for column, (label, value) in zip(columns, stats.items(), strict=False):
            metric_card(column, str(label), value)


def section_title(title: str) -> None:
    """Render a compact native section heading."""
    st.subheader(title)


def metric_card(column: Any, label: str, value: Any, help_text: str | None = None) -> None:
    """Render a consistent metric card in the provided Streamlit column."""
    with column.container(border=True):
        st.metric(label=label, value=value, help=help_text)


def nav_card(
    title: str,
    description: str,
    page: str,
    *,
    icon: str,
    label: str,
) -> None:
    """Render a native Streamlit navigation card."""
    with st.container(border=True):
        st.subheader(f"{icon} {title}")
        st.write(description)
        st.page_link(page, label=label, icon=icon)


def render_missing_data_error(error: Exception) -> None:
    """Show a user-friendly data loading error and stop page execution."""
    st.error(f"Unable to load IPL data: {error}")
    st.stop()
