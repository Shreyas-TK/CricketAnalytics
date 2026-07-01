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


def apply_global_styles() -> None:
    """Inject a cohesive theme for the dashboard."""
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 45%, #f8fafc 100%);
            }
            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 2rem;
            }
            .stMetric, .stAlert, .stInfo, .stSuccess, .stWarning, div[data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: 16px !important;
                background: rgba(255, 255, 255, 0.95) !important;
                backdrop-filter: blur(8px);
                box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
                border: 1px solid rgba(148, 163, 184, 0.25) !important;
            }
            .stButton > button {
                border-radius: 999px;
                border: none;
                background: linear-gradient(90deg, #14b8a6, #38bdf8);
                color: white;
                font-weight: 600;
                padding: 0.5rem 1rem;
            }
            .stButton > button:hover {
                box-shadow: 0 8px 20px rgba(56, 189, 248, 0.25);
                transform: translateY(-1px);
            }
            .stSelectbox > div, .stTextInput > div, .stNumberInput > div {
                border-radius: 10px;
            }
            .stTabs [data-testid="stTab"] {
                border-radius: 999px;
                padding: 0.4rem 0.8rem;
            }
            .stTabs [data-testid="stTab"][aria-selected="true"] {
                background: rgba(20, 184, 166, 0.16);
                color: #a7f3d0;
            }
            h1, h2, h3 {
                color: #0f172a;
            }
            .stMarkdown p, .stMarkdown li, .stCaption {
                color: #334155;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def configure_page(title: str, icon: str) -> None:
    """Apply consistent Streamlit page configuration."""
    st.set_page_config(
        page_title=f"{title} | IPL Cricket Analytics",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_global_styles()


def apply_theme() -> None:
    """Deprecated theme hook kept for backward compatibility."""
    return None


@st.cache_data(show_spinner=False)
def get_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load IPL data once per Streamlit session."""
    return load_data()


def render_sidebar() -> None:
    """Render shared sidebar context to provide a consistent experience."""
    with st.sidebar:
        st.markdown("## IPL Cricket Analytics")
        st.write(
            "Explore team, player, bowler, venue, and machine learning insights from IPL match data."
        )
        st.divider()
        st.write("**Tips**")
        st.write("- Use the top page menu to switch analytics views.")
        st.write("- Hover over charts for extra detail.")
        st.write("- Refresh the page if the data loader stalls.")
        st.divider()
        st.caption("Built for fast, interactive cricket analysis.")


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
        st.markdown(
            f"<div style='font-size:1rem; color:#6c757d; margin-bottom:0.75rem;'>{description}</div>",
            unsafe_allow_html=True,
        )
    if stats:
        columns = st.columns(len(stats), gap="medium")
        for column, (label, value) in zip(columns, stats.items(), strict=False):
            metric_card(column, str(label), value)


def section_title(title: str) -> None:
    """Render a compact native section heading."""
    st.subheader(title)


def metric_card(column: Any, label: str, value: Any, help_text: str | None = None) -> None:
    """Render a consistent metric card in the provided Streamlit column."""
    with column.container():
        st.markdown(
            f"""
            <div style="border:1px solid #e2e8f0; border-radius:14px; padding:14px 16px; background:#ffffff; margin-bottom:6px;">
                <div style="font-size:0.9rem; color:#64748b; margin-bottom:4px;">{label}</div>
                <div style="font-size:1.15rem; font-weight:700; color:#0f172a;">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if help_text:
            st.caption(help_text)


def nav_card(
    title: str,
    description: str,
    page: str,
    *,
    icon: str,
    label: str,
) -> None:
    """Render a native Streamlit navigation card."""
    with st.container():
        st.markdown(
            f"""
            <div style="border:1px solid #e2e8f0; border-radius:16px; padding:18px; background:linear-gradient(135deg, #ffffff, #f8fafc); margin-bottom:16px;">
                <h3 style="margin:0 0 8px 0; color:#0f172a;">{icon} {title}</h3>
                <p style="margin:0 0 12px 0; color:#475569; line-height:1.4;">{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.page_link(page, label=label, icon=icon)


def render_missing_data_error(error: Exception) -> None:
    """Show a user-friendly data loading error and stop page execution."""
    st.error(f"Unable to load IPL data: {error}")
    st.stop()
