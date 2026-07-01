import streamlit as st

from common import (
    configure_page,
    get_data,
    metric_card,
    render_page_header,
    render_missing_data_error,
    render_sidebar,
)
from src.ml.predictive_model import get_match_outcome_model, predict_match_winner

configure_page("Match Prediction", "🤖")
render_sidebar()

render_page_header("Match Prediction", "🤖", "Predict IPL match winners using historical match features.")

st.markdown(
    """
    Enhance match planning with data-driven prediction insights. Choose teams, toss conditions, and venue to see which side the model expects to win.
    """
)

try:
    with st.spinner("Loading IPL match data..."):
        matches, _ = get_data()
except Exception as exc:
    render_missing_data_error(exc)

teams = sorted(set(matches["team1"].dropna()).union(set(matches["team2"].dropna())))
venues = sorted(set(matches["venue"].dropna()))

with st.spinner("Loading prediction model..."):
    model, model_status = get_match_outcome_model(matches)

status_col, info_col = st.columns([2, 1], gap="large")
with status_col:
    st.metric("Model status", model_status)
    st.caption("Trained on historical IPL match results through 2025.")
with info_col:
    st.info(
        "**Tip:** Compare toss decisions and venue selections to explore how they affect predicted outcomes."
    )

st.divider()

st.subheader("Match inputs")
input_col1, input_col2 = st.columns(2, gap="large")
with input_col1:
    team1 = st.selectbox("Home Team", teams, index=0)
    team2 = st.selectbox("Away Team", teams, index=1)
    venue = st.selectbox("Venue", venues, index=0)

with input_col2:
    toss_winner = st.radio("Toss Winner", [team1, team2], horizontal=True)
    toss_decision = st.radio("Toss Decision", ["bat", "field"], horizontal=True)
    match_year = st.number_input(
        "Match Year",
        min_value=2008,
        max_value=2026,
        value=2025,
        help="Use the most recent season to see the latest expected performance trends.",
    )

st.divider()

summary_col1, summary_col2, summary_col3 = st.columns(3, gap="large")
summary_col1.metric("Home Team", team1)
summary_col2.metric("Away Team", team2)
summary_col3.metric("Venue", venue)

button_col1, button_col2 = st.columns([2, 1], gap="large")
with button_col1:
    if st.button("Predict Winner", type="primary"):
        prediction = predict_match_winner(
            model,
            team1=team1,
            team2=team2,
            venue=venue,
            toss_winner_is_team1=(toss_winner == team1),
            toss_decision_bat=(toss_decision == "bat"),
            match_year=match_year,
        )
        st.success(f"Predicted winner: {prediction}")
with button_col2:
    st.metric("Toss decision", toss_decision.title())
    st.metric("Toss winner", toss_winner)

with st.expander("How this prediction works"):
    st.write(
        "The model uses team matchups, venue patterns, toss outcomes, and season timing to estimate the likely winner of an IPL match. "
        "It is trained on historical IPL match data and refreshed from local persistence for fast predictions."
    )
