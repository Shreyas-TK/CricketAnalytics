import streamlit as st

from common import (
    configure_page,
    get_data,
    metric_card,
    render_page_header,
    render_missing_data_error,
    render_sidebar,
)
from src.analytics.batting import (
    player_batting_summary,
    player_dismissal_types,
    player_highest_score,
    player_milestones,
    player_runs_against_teams,
    player_runs_by_season,
    player_runs_by_venue,
    player_scoring_distribution,
)
from src.visualizations.plotly_charts import horizontal_bar, line_chart, pie_chart

configure_page("Player Analytics", "🏏")
render_sidebar()

render_page_header("Player Analytics", "🏏")
st.info("Select a player to view an interactive batting performance summary and scoring breakdown.")

try:
    with st.spinner("Loading player data..."):
        matches, deliveries = get_data()
except Exception as exc:  # pragma: no cover - Streamlit runtime handling
    render_missing_data_error(exc)

player = st.selectbox(
    "Select Player",
    sorted(deliveries["batsman"].dropna().unique()),
)

with st.spinner(f"Calculating batting metrics for {player}..."):
    summary = player_batting_summary(deliveries, player)
    highest = player_highest_score(deliveries, player)
    milestones = player_milestones(deliveries, player)

col1, col2, col3, col4 = st.columns(4, gap="medium")
metric_card(col1, "Runs", f"{summary['Runs']:,}")
metric_card(col2, "Matches", f"{summary['Matches']:,}")
metric_card(col3, "Average", summary["Average"])
metric_card(col4, "Strike Rate", summary["Strike Rate"])

col5, col6, col7, col8 = st.columns(4, gap="medium")
metric_card(col5, "Highest Score", highest)
metric_card(col6, "50s", milestones["50s"])
metric_card(col7, "100s", milestones["100s"])
metric_card(col8, "Boundary %", f"{summary['Boundary %']}%")

st.divider()

st.markdown("### Player performance overview")

tab1, tab2, tab3 = st.tabs(["📈 Career", "🎯 Matchups", "📊 Scoring"])

with tab1:
    with st.spinner("Building career trend..."):
        season_runs = player_runs_by_season(deliveries, matches, player)
    st.plotly_chart(
        line_chart(season_runs, "season", "batsman_runs", "Runs by Season"),
        use_container_width=True,
    )

with tab2:
    col1, col2 = st.columns(2, gap="large")
    with st.spinner("Building opposition and venue splits..."):
        team_runs = player_runs_against_teams(deliveries, player)
        venue_runs = player_runs_by_venue(deliveries, matches, player)

    with col1:
        st.plotly_chart(
            horizontal_bar(
                team_runs,
                "batsman_runs",
                "bowling_team",
                "Runs Against Teams",
            ),
            use_container_width=True,
        )

    with col2:
        st.plotly_chart(
            horizontal_bar(
                venue_runs.head(15),
                "batsman_runs",
                "venue",
                "Runs by Venue",
            ),
            use_container_width=True,
        )

with tab3:
    col1, col2 = st.columns(2, gap="large")
    with st.spinner("Building scoring distribution..."):
        dismissals = player_dismissal_types(deliveries, player)
        score_distribution = player_scoring_distribution(deliveries, player)

    with col1:
        if dismissals.empty:
            st.info("No dismissal data available for this player.")
        else:
            st.plotly_chart(
                pie_chart(
                    dismissals,
                    "dismissal_kind",
                    "dismissals",
                    "Dismissal Types",
                ),
                use_container_width=True,
            )

    with col2:
        st.plotly_chart(
            horizontal_bar(
                score_distribution,
                "Frequency",
                "Runs Scored",
                "Scoring Distribution",
            ),
            use_container_width=True,
        )
