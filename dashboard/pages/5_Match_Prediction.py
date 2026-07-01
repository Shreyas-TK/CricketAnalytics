import streamlit as st

from common import (
    configure_page,
    get_data,
    metric_card,
    render_page_header,
    render_missing_data_error,
    render_sidebar,
)
from src.ml.predictive_model import build_match_outcome_model, predict_match_winner

configure_page("Match Prediction", "🤖")
render_sidebar()

render_page_header("Match Prediction", "🤖", "Predict IPL match winners using historical match features.")

try:
    with st.spinner("Loading IPL match data..."):
        matches, _ = get_data()
except Exception as exc:
    render_missing_data_error(exc)

teams = sorted(set(matches["team1"].dropna()).union(set(matches["team2"].dropna())))
venues = sorted(set(matches["venue"].dropna()))

with st.spinner("Training prediction model..."):
    model, accuracy = build_match_outcome_model(matches)

st.metric("Model accuracy", f"{accuracy:.2%}")

team1 = st.selectbox("Home Team", teams, index=0)
team2 = st.selectbox("Away Team", teams, index=1)
venue = st.selectbox("Venue", venues, index=0)

col1, col2 = st.columns(2, gap="large")
with col1:
    toss_winner = st.radio("Toss Winner", [team1, team2], horizontal=True)
with col2:
    toss_decision = st.radio("Toss Decision", ["bat", "field"], horizontal=True)

match_year = st.number_input("Match Year", min_value=2008, max_value=2026, value=2025)

if st.button("Predict Winner"):
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
