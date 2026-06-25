"""Streamlit app for NPL2025 match outcome prediction."""

from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "NPL2025" / "outputs"
MODEL_PATH = OUTPUT_DIR / "logistic_regression_model.pkl"


def load_artifact() -> dict:
    with MODEL_PATH.open("rb") as handle:
        return pickle.load(handle)


def build_feature_frame(
    toss_decision: str,
    powerplay_runs: float,
    death_over_runs: float,
    total_wickets: float,
    boundary_count: float,
    dot_ball_count: float,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "toss_decision_encoded": 1 if toss_decision == "bat" else 0,
                "powerplay_runs": powerplay_runs,
                "death_over_runs": death_over_runs,
                "total_wickets": total_wickets,
                "boundary_count": boundary_count,
                "dot_ball_count": dot_ball_count,
            }
        ]
    )


def main() -> None:
    st.set_page_config(page_title="NPL 2025 Match Outcome Predictor", layout="wide")
    st.title("NPL 2025 Match Outcome Predictor")
    st.caption("Predicts whether the batting side or bowling side is more likely to win based on match features.")

    if not MODEL_PATH.exists():
        st.error("Trained model not found. Run `python NPL2025\\model.py` first to create `NPL2025\\outputs\\logistic_regression_model.pkl`.")
        st.stop()

    artifact = load_artifact()
    model = artifact["model"]
    feature_columns = artifact["feature_columns"]
    class_labels = artifact["class_labels"]

    st.sidebar.header("Match inputs")
    toss_decision = st.sidebar.selectbox("Toss decision", ["bat", "field"])
    powerplay_runs = st.sidebar.number_input("Powerplay runs", min_value=0.0, value=40.0, step=1.0)
    death_over_runs = st.sidebar.number_input("Death over runs", min_value=0.0, value=25.0, step=1.0)
    total_wickets = st.sidebar.number_input("Total wickets lost", min_value=0.0, value=6.0, step=1.0)
    boundary_count = st.sidebar.number_input("Boundary count", min_value=0.0, value=15.0, step=1.0)
    dot_ball_count = st.sidebar.number_input("Dot ball count", min_value=0.0, value=45.0, step=1.0)

    features = build_feature_frame(
        toss_decision,
        powerplay_runs,
        death_over_runs,
        total_wickets,
        boundary_count,
        dot_ball_count,
    )[feature_columns]

    if st.sidebar.button("Predict"):
        batting_probability = float(model.predict_proba(features)[0][1])
        bowling_probability = 1.0 - batting_probability
        predicted_class = int(model.predict(features)[0])
        predicted_side = class_labels[predicted_class]
        predicted_probability = batting_probability if predicted_class == 1 else bowling_probability

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Predicted side to win", predicted_side)
            st.metric("Win probability", f"{predicted_probability * 100:.2f}%")
        with col2:
            chart_df = pd.DataFrame(
                {
                    "Side": ["Batting team", "Bowling team"],
                    "Win Probability": [batting_probability, bowling_probability],
                }
            ).set_index("Side")

            fig, ax = plt.subplots(figsize=(6, 4))
            chart_df["Win Probability"].plot(kind="bar", ax=ax, color=["#1f77b4", "#ff7f0e"])
            ax.set_ylim(0, 1)
            ax.set_ylabel("Probability")
            ax.set_title("Win Probability by Side")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            st.pyplot(fig)
    else:
        st.info("Set the inputs in the sidebar and click Predict to see the result.")


if __name__ == "__main__":
    main()
