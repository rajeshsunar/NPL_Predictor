"""Load Cricsheet-style CSVs into match and delivery tables."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR.parent
OUTPUT_DIR = BASE_DIR / "outputs"

MATCH_COLUMNS = [
    "match_id",
    "date",
    "team1",
    "team2",
    "toss_winner",
    "toss_decision",
    "winner",
    "winner_wickets",
    "player_of_match",
    "venue",
    "city",
]

DELIVERY_COLUMNS = [
    "match_id",
    "innings",
    "over_ball",
    "batting_team",
    "batsman",
    "non_striker",
    "bowler",
    "batsman_runs",
    "extras",
    "wides",
    "noballs",
    "byes",
    "legbyes",
    "penalty",
    "wicket_type",
    "player_dismissed",
]


def _first_value(values: list[str]) -> str | None:
    return values[0] if values else None


def parse_match_file(csv_path: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    match_id = csv_path.stem

    teams: list[str] = []
    meta: dict[str, list[str]] = {}
    deliveries: list[dict[str, object]] = []

    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if not row:
                continue

            row_type = row[0]

            if row_type == "info":
                key = row[1] if len(row) > 1 else ""
                values = row[2:]
                if key == "team" and values:
                    teams.append(values[0])
                elif values:
                    meta.setdefault(key, []).append(values[0])
                continue

            if row_type != "ball":
                continue

            deliveries.append(
                {
                    "match_id": match_id,
                    "innings": row[1] if len(row) > 1 else None,
                    "over_ball": row[2] if len(row) > 2 else None,
                    "batting_team": row[3] if len(row) > 3 else None,
                    "batsman": row[4] if len(row) > 4 else None,
                    "non_striker": row[5] if len(row) > 5 else None,
                    "bowler": row[6] if len(row) > 6 else None,
                    "batsman_runs": row[7] if len(row) > 7 else None,
                    "extras": row[8] if len(row) > 8 else None,
                    "wides": row[9] if len(row) > 9 and row[9] != "" else None,
                    "noballs": row[10] if len(row) > 10 and row[10] != "" else None,
                    "byes": row[11] if len(row) > 11 and row[11] != "" else None,
                    "legbyes": row[12] if len(row) > 12 and row[12] != "" else None,
                    "penalty": row[13] if len(row) > 13 and row[13] != "" else None,
                    "wicket_type": row[14] if len(row) > 14 and row[14] != "" else None,
                    "player_dismissed": row[15] if len(row) > 15 and row[15] != "" else None,
                }
            )

    match = {
        "match_id": match_id,
        "date": _first_value(meta.get("date", [])),
        "team1": teams[0] if len(teams) > 0 else None,
        "team2": teams[1] if len(teams) > 1 else None,
        "toss_winner": _first_value(meta.get("toss_winner", [])),
        "toss_decision": _first_value(meta.get("toss_decision", [])),
        "winner": _first_value(meta.get("winner", [])),
        "winner_wickets": _first_value(meta.get("winner_wickets", [])),
        "player_of_match": _first_value(meta.get("player_of_match", [])),
        "venue": _first_value(meta.get("venue", [])),
        "city": _first_value(meta.get("city", [])),
    }

    return match, deliveries


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    csv_files = sorted(INPUT_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {INPUT_DIR}")

    match_rows: list[dict[str, object]] = []
    delivery_rows: list[dict[str, object]] = []

    for csv_path in csv_files:
        match_row, rows = parse_match_file(csv_path)
        match_rows.append(match_row)
        delivery_rows.extend(rows)

    matches_df = pd.DataFrame(match_rows, columns=MATCH_COLUMNS)
    deliveries_df = pd.DataFrame(delivery_rows, columns=DELIVERY_COLUMNS)

    matches_df["winner_wickets"] = pd.to_numeric(matches_df["winner_wickets"], errors="coerce").astype("Int64")
    for column in ["innings", "batsman_runs", "extras", "wides", "noballs", "byes", "legbyes", "penalty"]:
        deliveries_df[column] = pd.to_numeric(deliveries_df[column], errors="coerce").astype("Int64")

    return matches_df, deliveries_df


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    matches_df, deliveries_df = load_data()
    matches_df.to_csv(OUTPUT_DIR / "matches.csv", index=False)
    deliveries_df.to_csv(OUTPUT_DIR / "deliveries.csv", index=False)


if __name__ == "__main__":
    main()
