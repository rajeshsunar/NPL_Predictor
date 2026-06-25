"""Modeling utilities for NPL2025."""

from pathlib import Path
import math
import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency, f_oneway
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
MODEL_PATH = OUTPUT_DIR / "logistic_regression_model.pkl"


def load_match_features() -> pd.DataFrame:
    return pd.read_csv(OUTPUT_DIR / "match_features.csv")


def add_batting_side_flag(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["batting_team"] = pd.NA

    bat_mask = df["toss_decision"].astype("string").str.lower().eq("bat")
    field_mask = df["toss_decision"].astype("string").str.lower().eq("field")

    df.loc[bat_mask, "batting_team"] = df.loc[bat_mask, "toss_winner"]

    batting_team1_mask = field_mask & df["toss_winner"].eq(df["team1"])
    batting_team2_mask = field_mask & df["toss_winner"].eq(df["team2"])
    df.loc[batting_team1_mask, "batting_team"] = df.loc[batting_team1_mask, "team2"]
    df.loc[batting_team2_mask, "batting_team"] = df.loc[batting_team2_mask, "team1"]

    df["batting_side_flag"] = pd.NA
    df.loc[df["winner"] == df["batting_team"], "batting_side_flag"] = 1
    df.loc[df["winner"].notna() & df["batting_team"].notna() & (df["winner"] != df["batting_team"]), "batting_side_flag"] = 0
    df["batting_side_flag"] = pd.to_numeric(df["batting_side_flag"], errors="coerce")
    return df


def compute_vif(frame: pd.DataFrame) -> pd.DataFrame:
    numeric = frame.select_dtypes(include="number").copy()
    numeric = numeric.loc[:, numeric.nunique(dropna=True) > 1]
    numeric = numeric.dropna()

    if numeric.empty:
        return pd.DataFrame(columns=["feature", "vif"])

    vif_rows = []
    for index, column in enumerate(numeric.columns):
        vif_rows.append({"feature": column, "vif": variance_inflation_factor(numeric.values, index)})

    return pd.DataFrame(vif_rows).sort_values("vif", ascending=False)


def chi_square_toss_vs_winner(df: pd.DataFrame) -> tuple[float, float, int, pd.DataFrame]:
    pairs = df[["toss_winner", "winner"]].dropna()
    contingency = pd.crosstab(pairs["toss_winner"], pairs["winner"])
    chi2, p_value, dof, _ = chi2_contingency(contingency)
    return chi2, p_value, dof, contingency


def one_way_anova_first_innings_runs(df: pd.DataFrame) -> tuple[float, float, pd.Series]:
    pairs = df[["team1", "innings1_total_runs"]].dropna()
    grouped = pairs.groupby("team1")["innings1_total_runs"]
    samples = [values.to_numpy() for _, values in grouped if len(values) > 1]
    counts = grouped.size()
    if len(samples) < 2:
        return float("nan"), float("nan"), counts
    f_statistic, p_value = f_oneway(*samples)
    return f_statistic, p_value, counts


def prepare_logistic_data(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    frame["toss_decision_encoded"] = frame["toss_decision"].map({"bat": 1, "field": 0})
    frame = frame.rename(
        columns={
            "innings1_powerplay_runs": "powerplay_runs",
            "innings1_death_over_runs": "death_over_runs",
            "innings1_total_wickets": "total_wickets",
            "innings1_boundary_count": "boundary_count",
            "innings1_dot_ball_count": "dot_ball_count",
        }
    )

    required_columns = [
        "batting_side_flag",
        "toss_decision_encoded",
        "powerplay_runs",
        "death_over_runs",
        "total_wickets",
        "boundary_count",
        "dot_ball_count",
    ]
    frame = frame[required_columns].dropna()
    frame["batting_side_flag"] = frame["batting_side_flag"].astype(int)
    return frame


def save_roc_curve(y_true: pd.Series, y_prob: pd.Series, output_path: Path) -> float:
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    auc_score = roc_auc_score(y_true, y_prob)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f"ROC curve (AUC = {auc_score:.4f})")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random chance")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve for Logistic Regression")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    return auc_score


def save_probability_distribution(y_true: pd.Series, y_prob: pd.Series, output_path: Path) -> None:
    plot_df = pd.DataFrame(
        {
            "batting_side_flag": y_true.map({0: "Bowling team", 1: "Batting team"}),
            "predicted_probability": y_prob,
        }
    )

    plt.figure(figsize=(8, 6))
    sns.histplot(
        data=plot_df,
        x="predicted_probability",
        hue="batting_side_flag",
        bins=10,
        kde=True,
        stat="density",
        common_norm=False,
        element="step",
    )
    plt.xlabel("Predicted probability of batting_side_flag = 1")
    plt.ylabel("Density")
    plt.title("Predicted Probability Distribution by Class")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def main() -> None:
    df = add_batting_side_flag(load_match_features())

    valid = df["batting_side_flag"].notna()
    if valid.sum() != len(df):
        print(f"Dropped {len(df) - valid.sum()} rows without a valid batting-side winner match.")

    df = df.loc[valid].copy()
    df["batting_side_flag"] = df["batting_side_flag"].astype(int)

    chi2, p_value, dof, contingency = chi_square_toss_vs_winner(df)
    print("Chi-square test for toss_winner vs winner:")
    print(contingency)
    print(f"Chi-square statistic: {chi2:.4f}")
    print(f"p-value: {p_value:.4f}")
    if p_value < 0.05:
        print("Interpretation: Reject the null hypothesis. Toss winning significantly affects match outcome at the 95% confidence level.")
    else:
        print("Interpretation: Fail to reject the null hypothesis. Toss winning does not significantly affect match outcome at the 95% confidence level.")
    print()

    f_statistic, anova_p_value, team_counts = one_way_anova_first_innings_runs(df)
    print("One-way ANOVA for innings1_total_runs across teams:")
    print(team_counts)
    print(f"F-statistic: {f_statistic:.4f}")
    print(f"p-value: {anova_p_value:.4f}")
    if anova_p_value < 0.05:
        print("Interpretation: Reject the null hypothesis. Mean first innings runs differ significantly across NPL teams at the 95% confidence level.")
    else:
        print("Interpretation: Fail to reject the null hypothesis. Mean first innings runs do not differ significantly across NPL teams at the 95% confidence level.")
    print()

    logistic_df = prepare_logistic_data(df)
    feature_columns = [
        "toss_decision_encoded",
        "powerplay_runs",
        "death_over_runs",
        "total_wickets",
        "boundary_count",
        "dot_ball_count",
    ]
    X = logistic_df[feature_columns]
    y = logistic_df["batting_side_flag"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = pd.Series(model.predict_proba(X_test)[:, 1], index=X_test.index)
    with MODEL_PATH.open("wb") as handle:
        pickle.dump(
            {
                "model": model,
                "feature_columns": feature_columns,
                "class_labels": {0: "Bowling team", 1: "Batting team"},
            },
            handle,
        )

    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, zero_division=0)

    coefficients = pd.DataFrame(
        {
            "feature": feature_columns,
            "coefficient": model.coef_[0],
        }
    )
    coefficients["odds_ratio"] = coefficients["coefficient"].map(math.exp)

    sm_model = sm.Logit(y_train, sm.add_constant(X_train)).fit(disp=False)
    p_values = sm_model.pvalues.rename("p_value").reset_index().rename(columns={"index": "feature"})
    p_values.loc[p_values["feature"] == "const", "feature"] = "intercept"

    coefficient_summary = coefficients.merge(p_values, on="feature", how="left")
    auc_score = save_roc_curve(y_test, y_prob, OUTPUT_DIR / "logistic_regression_roc_curve.png")
    save_probability_distribution(y_test, y_prob, OUTPUT_DIR / "predicted_probability_distribution.png")

    h3_statistic = sm_model.llr
    h3_p_value = sm_model.llr_pvalue
    h4_statistic = sm_model.tvalues["toss_decision_encoded"]
    h4_p_value = sm_model.pvalues["toss_decision_encoded"]

    hypothesis_summary = pd.DataFrame(
        [
            {
                "Hypothesis": "H1",
                "Test used": "Chi-square test of independence",
                "Test statistic": chi2,
                "p-value": p_value,
                "Decision": "Supported" if p_value < 0.05 else "Rejected",
            },
            {
                "Hypothesis": "H2",
                "Test used": "One-way ANOVA",
                "Test statistic": f_statistic,
                "p-value": anova_p_value,
                "Decision": "Supported" if anova_p_value < 0.05 else "Rejected",
            },
            {
                "Hypothesis": "H3",
                "Test used": "Logistic regression overall likelihood ratio test",
                "Test statistic": h3_statistic,
                "p-value": h3_p_value,
                "Decision": "Supported" if h3_p_value < 0.05 else "Rejected",
            },
            {
                "Hypothesis": "H4",
                "Test used": "Logistic regression coefficient test for toss_decision_encoded",
                "Test statistic": h4_statistic,
                "p-value": h4_p_value,
                "Decision": "Supported" if h4_p_value < 0.05 else "Rejected",
            },
        ]
    )

    print("Logistic Regression results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"AUC score: {auc_score:.4f}")
    print("Confusion matrix:")
    print(cm)
    print("Classification report:")
    print(report)
    print("Coefficients and odds ratios:")
    print(coefficient_summary)
    print("Statsmodels logit p-values:")
    print(p_values)
    print()

    print("Diagnostic plots saved:")
    print(OUTPUT_DIR / "logistic_regression_roc_curve.png")
    print(OUTPUT_DIR / "predicted_probability_distribution.png")
    print(MODEL_PATH)
    print()

    print("Hypothesis summary:")
    print(hypothesis_summary.to_string(index=False, float_format=lambda value: f"{value:.4f}"))
    print()

    numeric = df.select_dtypes(include="number").drop(columns=["match_id", "batting_side_flag"], errors="ignore")
    numeric = numeric.loc[:, numeric.nunique(dropna=True) > 1]
    correlation_values = {}
    for column in numeric.columns:
        paired = df[[column, "batting_side_flag"]].dropna()
        if paired[column].nunique(dropna=True) < 2 or paired["batting_side_flag"].nunique(dropna=True) < 2:
            continue
        correlation_values[column] = paired[column].corr(paired["batting_side_flag"])

    correlations = pd.Series(correlation_values).sort_values(key=lambda s: s.abs(), ascending=False)

    vif_input = numeric.copy()
    vif_input = vif_input.dropna()
    vif = compute_vif(vif_input)

    print("Correlation with batting_side_flag:")
    print(correlations)
    print()

    print("VIF scores:")
    print(vif)
    print()

    relevant_features = pd.DataFrame(
        {
            "correlation": correlations,
            "abs_correlation": correlations.abs(),
        }
    ).join(vif.set_index("feature"), how="left")
    relevant_features = relevant_features.sort_values(
        by=["abs_correlation", "vif"], ascending=[False, True]
    )

    print("Most relevant features (high |correlation|, lower VIF preferred):")
    print(relevant_features.head(10))


if __name__ == "__main__":
    main()
