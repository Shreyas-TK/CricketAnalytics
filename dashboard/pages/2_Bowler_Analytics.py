import streamlit as st

from common import (
    configure_page,
    get_data,
    metric_card,
    render_page_header,
    render_missing_data_error,
    render_sidebar,
)
from src.analytics.bowling import (
    best_bowling_figures,
    bowler_summary,
    bowling_milestones,
    wickets_against_teams,
    wickets_by_season,
    wickets_by_venue,
)
from src.visualizations.plotly_charts import horizontal_bar, line_chart

configure_page("Bowler Analytics", "🎯")
render_sidebar()

render_page_header("Bowler Analytics", "🎯")
st.info("View bowler efficiency, wickets, and venue impact with clear metrics and charts.")

try:
    with st.spinner("Loading bowler data..."):
        matches, deliveries = get_data()
except Exception as exc:  # pragma: no cover - Streamlit runtime handling
    render_missing_data_error(exc)

bowler = st.selectbox(
    "Select Bowler",
    sorted(deliveries["bowler"].dropna().unique()),
)

with st.spinner(f"Calculating bowling metrics for {bowler}..."):
    summary = bowler_summary(deliveries, bowler)
    best = best_bowling_figures(deliveries, bowler)
    milestones = bowling_milestones(deliveries, bowler)

col1, col2, col3, col4 = st.columns(4, gap="medium")
metric_card(col1, "Matches", f"{summary['Matches']:,}")
metric_card(col2, "Wickets", f"{summary['Wickets']:,}")
metric_card(col3, "Economy", summary["Economy"])
metric_card(col4, "Average", summary["Average"])

col5, col6, col7, col8 = st.columns(4, gap="medium")
metric_card(col5, "Overs", summary["Overs"])
metric_card(col6, "Runs Conceded", f"{summary['Runs']:,}")
metric_card(col7, "Strike Rate", summary["Strike Rate"])
metric_card(col8, "Best Bowling", best)

st.divider()

st.markdown("### Bowler performance overview")

tab1, tab2, tab3 = st.tabs(["📈 Career", "🏏 Matchups", "🏅 Milestones"])

with tab1:
    with st.spinner("Building wicket trend..."):
        season_wickets = wickets_by_season(deliveries, matches, bowler)
    st.plotly_chart(
        line_chart(season_wickets, "season", "wickets", "Wickets by Season"),
        use_container_width=True,
    )

with tab2:
    col1, col2 = st.columns(2, gap="large")
    with st.spinner("Building opposition and venue splits..."):
        team_wickets = wickets_against_teams(deliveries, bowler)
        venue_wickets = wickets_by_venue(deliveries, matches, bowler)

    with col1:
        st.plotly_chart(
            horizontal_bar(
                team_wickets,
                "wickets",
                "batting_team",
                "Wickets Against Teams",
            ),
            use_container_width=True,
        )

    with col2:
        st.plotly_chart(
            horizontal_bar(
                venue_wickets.head(15),
                "wickets",
                "venue",
                "Wickets by Venue",
            ),
            use_container_width=True,
        )

with tab3:
    c1, c2, c3 = st.columns(3, gap="medium")
    metric_card(c1, "Best Bowling", best)
    metric_card(c2, "3 Wicket Hauls", milestones["3W"])
    metric_card(c3, "5 Wicket Hauls", milestones["5W"])
