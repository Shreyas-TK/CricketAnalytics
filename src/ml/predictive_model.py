from __future__ import annotations


from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score


MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "match_predictor.joblib"


def _ensure_model_dir() -> None:
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)


def save_match_outcome_model(model: Pipeline) -> None:
    """Save the trained match prediction model to disk."""
    _ensure_model_dir()
    joblib.dump(model, MODEL_PATH)


def load_saved_match_outcome_model() -> Pipeline | None:
    """Load a previously saved match prediction model if available."""
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None


def _prepare_feature_data(matches: pd.DataFrame) -> pd.DataFrame:
    df = matches.copy()
    df = df.dropna(subset=["team1", "team2", "toss_winner", "toss_decision", "winner"])
    df = df[df["winner"].isin(df[["team1", "team2"]].stack())]

    df["match_year"] = pd.to_datetime(df["date"], errors="coerce").dt.year
    df["toss_winner_is_team1"] = (df["toss_winner"] == df["team1"]).astype(int)
    df["toss_decision_bat"] = (df["toss_decision"] == "bat").astype(int)
    df["venue"] = df["venue"].fillna("Unknown")

    target = df["winner"]
    features = df[["team1", "team2", "venue", "toss_winner_is_team1", "toss_decision_bat", "match_year"]].copy()
    features["team1"] = features["team1"].astype(str)
    features["team2"] = features["team2"].astype(str)
    features["venue"] = features["venue"].astype(str)
    features["match_year"] = features["match_year"].fillna(features["match_year"].median())

    return features, target


def build_match_outcome_model(matches: pd.DataFrame) -> tuple[Pipeline, dict[str, Any]]:
    features, target = _prepare_feature_data(matches)
    categorical_features = ["team1", "team2", "venue"]
    numeric_features = ["toss_winner_is_team1", "toss_decision_bat", "match_year"]

    preprocess = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numeric_features),
        ]
    )

    pipeline = Pipeline(
    steps=[("preprocess", preprocess), ("clf", RandomForestClassifier(random_state=42, n_estimators=200, class_weight="balanced"))]
    )

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42, stratify=target)
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    accuracy = float(accuracy_score(y_test, predictions))
    f1 = float(f1_score(y_test, predictions, average="weighted"))
    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)
    matrix = confusion_matrix(y_test, predictions)
    metrics = {
        "accuracy": accuracy,
        "f1_weighted": f1,
        "classification_report": report,
        "confusion_matrix": matrix,
    }
    return pipeline, metrics


def get_match_outcome_model(matches: pd.DataFrame) -> tuple[Pipeline, str]:
    """Load an existing model if available, otherwise train and save a new one."""
    model = load_saved_match_outcome_model()
    if model is not None:
        return model, "Saved model loaded"

    model, metrics = build_match_outcome_model(matches)
    save_match_outcome_model(model)
    return model, f"Accuracy {metrics['accuracy']:.2%} | F1 {metrics['f1_weighted']:.2%}"


def explain_model_features(model: Pipeline, matches: pd.DataFrame) -> list[dict[str, Any]]:
    """Return model feature-importance values for recruiter-friendly explainability."""
    features, _ = _prepare_feature_data(matches)
    classifier = model.named_steps["clf"]
    feature_names = model.named_steps["preprocess"].get_feature_names_out()
    importances = getattr(classifier, "feature_importances_", None)
    if importances is None:
        return []

    ranked = sorted(
        zip(feature_names, importances, strict=False),
        key=lambda item: item[1],
        reverse=True,
    )
    return [
        {"feature": feature, "importance": float(importance)}
        for feature, importance in ranked[:10]
    ]


def predict_match_winner(model: Pipeline, team1: str, team2: str, venue: str, toss_winner_is_team1: bool, toss_decision_bat: bool, match_year: int) -> Any:
    row = pd.DataFrame(
        [
            {
                "team1": team1,
                "team2": team2,
                "venue": venue,
                "toss_winner_is_team1": int(toss_winner_is_team1),
                "toss_decision_bat": int(toss_decision_bat),
                "match_year": match_year,
            }
        ]
    )
    return model.predict(row)[0]
