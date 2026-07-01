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
    team_summary,
    team_top_batter,
    team_top_bowler,
    team_win_by_season,
)
from src.visualizations.plotly_charts import horizontal_bar, line_chart

configure_page("Team Analytics", "🏆")
render_sidebar()

render_page_header("Team Analytics", "🏆")
st.info("Compare team performance and discover season trends, top batters, and leading bowlers.")

try:
    with st.spinner("Loading team data..."):
        matches, deliveries = get_data()
except Exception as exc:  # pragma: no cover - Streamlit runtime handling
    render_missing_data_error(exc)

teams = sorted(set(matches["team1"].dropna()).union(set(matches["team2"].dropna())))
team = st.selectbox("Select Team", teams)

with st.spinner(f"Calculating team metrics for {team}..."):
    summary = team_summary(matches, deliveries, team)

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
metric_card(col1, "Matches", f"{summary['Matches']:,}")
metric_card(col2, "Wins", f"{summary['Wins']:,}")
metric_card(col3, "Losses", f"{summary['Losses']:,}")
metric_card(col4, "Win %", f"{summary['Win %']}%")
metric_card(col5, "Toss Wins", f"{summary['Toss Wins']:,}")

st.divider()

st.markdown("### Team overview")

tab1, tab2 = st.tabs(["📈 Season Trend", "🏅 Top Players"])

with tab1:
    with st.spinner("Building season win trend..."):
        season = team_win_by_season(matches, team)
    st.plotly_chart(
        line_chart(season, "season", "win_pct", "Win % by Season"),
        use_container_width=True,
    )

with tab2:
    col1, col2 = st.columns(2, gap="large")
    with st.spinner("Building top player charts..."):
        batters = team_top_batter(deliveries, team)
        bowlers = team_top_bowler(deliveries, team)

    with col1:
        st.plotly_chart(
            horizontal_bar(
                batters,
                "batsman_runs",
                "batsman",
                "Top Run Scorers",
            ),
            use_container_width=True,
        )

    with col2:
        st.plotly_chart(
            horizontal_bar(
                bowlers,
                "wickets",
                "bowler",
                "Top Wicket Takers",
            ),
            use_container_width=True,
        )
