import streamlit as st

from common import (
    configure_page,
    get_data,
    metric_card,
    render_page_header,
    render_missing_data_error,
    render_sidebar,
)
from src.analytics.team import (
    highest_scoring_venues,
    venue_runs_by_season,
    venue_summary,
    venue_team_wins,
    venue_toss_impact,
)
from src.visualizations.plotly_charts import horizontal_bar, line_chart

configure_page("Venue Analytics", "🏟️")
render_sidebar()

render_page_header("Venue Analytics", "🏟️")
st.info("Select a venue to explore scoring trends, toss outcomes, and team performance at the ground.")

try:
    with st.spinner("Loading venue data..."):
        matches, deliveries = get_data()
except Exception as exc:  # pragma: no cover - Streamlit runtime handling
    render_missing_data_error(exc)

venue = st.selectbox(
    "Select Venue",
    sorted(matches["venue"].dropna().unique()),
)

with st.spinner(f"Calculating venue metrics for {venue}..."):
    summary = venue_summary(matches, deliveries, venue)

col1, col2, col3, col4 = st.columns(4, gap="medium")
metric_card(col1, "Matches", f"{summary['Matches']:,}")
metric_card(col2, "Avg Innings Score", summary["Avg Innings Score"])
metric_card(col3, "Highest Innings Score", summary["Highest Innings Score"])
metric_card(col4, "Toss Win Match Win %", f"{summary['Toss Win Match Win %']}%")

st.divider()

st.markdown("### Venue overview")

tab1, tab2 = st.tabs(["📈 Venue Trend", "🏆 Venue Leaders"])

with tab1:
    with st.spinner("Building venue scoring trend..."):
        season_scores = venue_runs_by_season(matches, deliveries, venue)

    if season_scores.empty:
        st.info("No season trend available for this venue.")
    else:
        st.plotly_chart(
            line_chart(
                season_scores,
                "season",
                "avg_score",
                "Average Innings Score by Season",
            ),
            use_container_width=True,
        )

with tab2:
    col1, col2, col3 = st.columns(3, gap="large")
    with st.spinner("Building venue leaderboards..."):
        team_wins = venue_team_wins(matches, venue)
        scoring_venues = highest_scoring_venues(matches, deliveries)
        toss_venues = venue_toss_impact(matches)

    with col1:
        st.plotly_chart(
            horizontal_bar(team_wins, "wins", "winner", "Most Wins at Venue"),
            use_container_width=True,
        )

    with col2:
        st.plotly_chart(
            horizontal_bar(
                scoring_venues,
                "avg_score",
                "venue",
                "Highest Scoring Venues",
            ),
            use_container_width=True,
        )

    with col3:
        st.plotly_chart(
            horizontal_bar(
                toss_venues,
                "toss_match_win_pct",
                "venue",
                "Toss Impact by Venue",
            ),
            use_container_width=True,
        )
