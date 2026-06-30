import streamlit as st

from common import (
    configure_page,
    get_data,
    metric_card,
    nav_card,
    render_page_header,
    render_missing_data_error,
    render_sidebar,
    section_title,
)
from src.analytics.team import highest_scoring_venues, team_win_percentage, toss_impact

configure_page("Overview", "🏏")
render_sidebar()

render_page_header("Overview", "🏏")

try:
    with st.spinner("Loading IPL match and delivery data..."):
        matches, deliveries = get_data()
except Exception as exc:  # pragma: no cover - Streamlit runtime handling
    render_missing_data_error(exc)

total_matches = len(matches)
total_deliveries = len(deliveries)
season_count = matches["season"].nunique()
team_count = (
    set(matches["team1"].dropna())
    .union(set(matches["team2"].dropna()))
)

section_title("Key Metrics")
col1, col2, col3, col4 = st.columns(4, gap="medium")
metric_card(col1, "Total Matches", f"{total_matches:,}")
metric_card(col2, "Total Deliveries", f"{total_deliveries:,}")
metric_card(col3, "Seasons Covered", f"{season_count}")
metric_card(col4, "Teams", f"{len(team_count)}")

section_title("Explore Analytics")
col1, col2 = st.columns(2, gap="large")

with col1:
    nav_card(
        "Player Analytics",
        "Batting records, scoring patterns, venues, and opposition splits.",
        "pages/1_Player_Analytics.py",
        icon="🏏",
        label="Open Player Analytics",
    )
    nav_card(
        "Bowler Analytics",
        "Wickets, economy, venue impact, and bowling milestones.",
        "pages/2_Bowler_Analytics.py",
        icon="🎯",
        label="Open Bowler Analytics",
    )

with col2:
    nav_card(
        "Team Analytics",
        "Team records, season trends, top batters, and top bowlers.",
        "pages/3_Team_Analytics.py",
        icon="🏆",
        label="Open Team Analytics",
    )
    nav_card(
        "Venue Analytics",
        "Venue scoring trends, toss impact, and team wins.",
        "pages/4_Venue_Analytics.py",
        icon="🏟️",
        label="Open Venue Analytics",
    )

with st.spinner("Calculating dashboard highlights..."):
    win_table = team_win_percentage(matches)
    venue_table = highest_scoring_venues(matches, deliveries, top_n=5)
    toss_win_pct = toss_impact(matches)

section_title("Dashboard Highlights")
highlight1, highlight2, highlight3 = st.columns(3, gap="medium")
metric_card(
    highlight1,
    "Best Win %",
    f"{win_table.iloc[0]['win_pct']:.2f}%",
    str(win_table.iloc[0]["team"]) if not win_table.empty else None,
)
metric_card(
    highlight2,
    "Top Scoring Venue",
    f"{venue_table.iloc[0]['avg_score']:.1f}",
    str(venue_table.iloc[0]["venue"]) if not venue_table.empty else None,
)
metric_card(highlight3, "Toss Winner Match Win %", f"{toss_win_pct:.2f}%")

