"""Exploratory data analysis entry point for NPL2025."""

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def build_match_features(matches: pd.DataFrame, deliveries: pd.DataFrame) -> pd.DataFrame:
    deliveries = deliveries.copy()
    deliveries["batsman_runs"] = pd.to_numeric(deliveries["batsman_runs"], errors="coerce").fillna(0)
    deliveries["extras"] = pd.to_numeric(deliveries["extras"], errors="coerce").fillna(0)
    deliveries["wicket_type"] = deliveries["wicket_type"].fillna("")
    deliveries["over_number"] = pd.to_numeric(deliveries["over_ball"], errors="coerce").fillna(0).astype(int)

    inning_features = (
        deliveries.assign(
            total_runs=deliveries["batsman_runs"] + deliveries["extras"],
            powerplay_runs=lambda df: (df["batsman_runs"] + df["extras"]) * df["over_number"].between(0, 5),
            death_over_runs=lambda df: (df["batsman_runs"] + df["extras"]) * df["over_number"].between(16, 19),
            total_wickets=lambda df: df["wicket_type"].ne(""),
            boundary_count=lambda df: df["batsman_runs"].isin([4, 6]),
            dot_ball_count=lambda df: df["batsman_runs"].eq(0) & df["extras"].eq(0),
        )
        .groupby(["match_id", "innings"], as_index=False)[
            [
                "total_runs",
                "powerplay_runs",
                "death_over_runs",
                "total_wickets",
                "boundary_count",
                "dot_ball_count",
            ]
        ]
        .sum()
    )

    wide_features = inning_features.pivot(index="match_id", columns="innings")
    wide_features.columns = [f"innings{innings}_{feature}" for feature, innings in wide_features.columns]
    wide_features = wide_features.reset_index()

    merged = matches.merge(wide_features, on="match_id", how="left")
    feature_columns = [column for column in merged.columns if column.startswith("innings")]
    merged[feature_columns] = merged[feature_columns].fillna(0).astype(int)
    return merged


def build_innings_totals(deliveries: pd.DataFrame) -> pd.DataFrame:
    deliveries = deliveries.copy()
    deliveries["batsman_runs"] = pd.to_numeric(deliveries["batsman_runs"], errors="coerce").fillna(0)
    deliveries["extras"] = pd.to_numeric(deliveries["extras"], errors="coerce").fillna(0)

    innings_totals = (
        deliveries.assign(innings_total_runs=deliveries["batsman_runs"] + deliveries["extras"])
        .groupby(["match_id", "innings", "batting_team"], as_index=False)["innings_total_runs"]
        .sum()
    )
    return innings_totals


def build_innings_scatter_data(match_features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for innings in range(1, 5):
        total_col = f"innings{innings}_total_runs"
        powerplay_col = f"innings{innings}_powerplay_runs"
        subset = match_features[[total_col, powerplay_col]].copy()
        subset = subset.rename(columns={total_col: "total_runs", powerplay_col: "powerplay_runs"})
        subset = subset[(subset["total_runs"] > 0) | (subset["powerplay_runs"] > 0)]
        rows.append(subset)

    if not rows:
        return pd.DataFrame(columns=["total_runs", "powerplay_runs"])

    return pd.concat(rows, ignore_index=True)


def save_plots(match_features: pd.DataFrame, deliveries: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    first_innings_runs = pd.to_numeric(match_features["innings1_total_runs"], errors="coerce").fillna(0)
    plt.figure(figsize=(8, 5))
    sns.histplot(first_innings_runs, bins=10, kde=True, color="steelblue")
    plt.title("Histogram of First Innings Runs")
    plt.xlabel("First Innings Runs")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "first_innings_runs_histogram.png", dpi=300)
    plt.close()

    innings_totals = build_innings_totals(deliveries)
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=innings_totals, x="batting_team", y="innings_total_runs", color="lightseagreen")
    plt.title("Total Runs by Team Across Innings")
    plt.xlabel("Batting Team")
    plt.ylabel("Innings Total Runs")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "team_total_runs_boxplot.png", dpi=300)
    plt.close()

    scatter_data = build_innings_scatter_data(match_features)
    plt.figure(figsize=(8, 6))
    sns.regplot(data=scatter_data, x="powerplay_runs", y="total_runs", scatter_kws={"alpha": 0.7}, line_kws={"color": "red"})
    plt.title("Powerplay Runs vs Total Innings Runs")
    plt.xlabel("Powerplay Runs")
    plt.ylabel("Total Innings Runs")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "powerplay_vs_total_runs_scatter.png", dpi=300)
    plt.close()

    toss_counts = match_features["toss_decision"].value_counts().reindex(["bat", "field"]).fillna(0)
    plt.figure(figsize=(6, 5))
    plt.bar(toss_counts.index, toss_counts.values, color=["#5b8ff9", "#61dDAa"])
    plt.title("Toss Decisions")
    plt.xlabel("Toss Decision")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "toss_decisions_bar_chart.png", dpi=300)
    plt.close()

    wicket_types = deliveries["wicket_type"].fillna("").str.strip().str.lower()
    wicket_counts = wicket_types[wicket_types.isin(["caught", "bowled", "lbw", "run out", "stumped"])].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(wicket_counts.values, labels=wicket_counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Wicket Types")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "wicket_types_pie_chart.png", dpi=300)
    plt.close()

    numeric_features = match_features.select_dtypes(include="number")
    corr = numeric_features.corr()
    plt.figure(figsize=(14, 10))
    sns.heatmap(corr, cmap="coolwarm", center=0, linewidths=0.5)
    plt.title("Correlation Heatmap of Match Features")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "match_features_correlation_heatmap.png", dpi=300)
    plt.close()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    matches = pd.read_csv(OUTPUT_DIR / "matches.csv")
    deliveries = pd.read_csv(OUTPUT_DIR / "deliveries.csv")

    print("matches shape:", matches.shape)
    print("deliveries shape:", deliveries.shape)
    print()

    print("matches columns:")
    print(matches.columns.tolist())
    print()
    print("deliveries columns:")
    print(deliveries.columns.tolist())
    print()

    print("matches head:")
    print(matches.head())
    print()
    print("deliveries head:")
    print(deliveries.head())
    print()

    print("matches missing values:")
    print(matches.isna().sum())
    print()
    print("deliveries missing values:")
    print(deliveries.isna().sum())
    print()

    print("matches describe:")
    print(matches.describe(include="all"))
    print()
    print("deliveries describe:")
    print(deliveries.describe(include="all"))

    match_features = build_match_features(matches, deliveries)
    match_features.to_csv(OUTPUT_DIR / "match_features.csv", index=False)
    print()
    print("match_features shape:", match_features.shape)

    match_features = pd.read_csv(OUTPUT_DIR / "match_features.csv")
    save_plots(match_features, deliveries)


if __name__ == "__main__":
    main()
