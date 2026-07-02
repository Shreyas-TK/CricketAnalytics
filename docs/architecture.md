# Architecture Overview

This project follows a simple, recruiter-friendly architecture:

1. Raw IPL data is loaded from CSV files.
2. A data loading layer standardizes and validates the input.
3. A processing layer creates reproducible processed datasets.
4. Analytics modules compute batting, bowling, team, and venue insights.
5. A Streamlit app surfaces the insights with Plotly charts and metrics.
6. A lightweight ML pipeline trains and evaluates a match outcome predictor.
