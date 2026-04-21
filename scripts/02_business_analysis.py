"""Create business summary tables from the cleaned dataset.

Run from the project root:
    python scripts/02_business_analysis.py
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "food_delivery_cleaned.csv"
OUTPUT_DIR = ROOT / "artifacts" / "analysis_outputs"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH, parse_dates=["order_datetime"])

    city_summary = (
        df.groupby("city")
        .agg(
            orders=("order_id", "count"),
            gross_profit=("gross_profit", "sum"),
            avg_margin_pct=("profit_margin_pct", "mean"),
            repeat_rate=("repeat_customer_flag", "mean"),
            delay_rate=("delivery_delay_flag", "mean"),
            avg_rating=("rating", "mean"),
        )
        .round(2)
        .sort_values("gross_profit", ascending=False)
    )

    discount_summary = (
        df.groupby("discount_band", observed=True)
        .agg(
            orders=("order_id", "count"),
            avg_discount=("discount_amount", "mean"),
            avg_profit=("gross_profit", "mean"),
            repeat_rate=("repeat_customer_flag", "mean"),
            avg_rating=("rating", "mean"),
        )
        .round(2)
    )

    zone_risk = (
        df.groupby(["city", "zone"])
        .agg(
            orders=("order_id", "count"),
            delay_rate=("delivery_delay_flag", "mean"),
            avg_delay_minutes=("delay_minutes", "mean"),
            avg_rating=("rating", "mean"),
            gross_profit=("gross_profit", "sum"),
        )
        .query("orders >= 30")
        .sort_values(["delay_rate", "avg_rating"], ascending=[False, True])
        .round(2)
    )

    city_summary.to_csv(OUTPUT_DIR / "city_summary.csv")
    discount_summary.to_csv(OUTPUT_DIR / "discount_summary.csv")
    zone_risk.to_csv(OUTPUT_DIR / "zone_risk_summary.csv")

    print("Saved business analysis outputs:")
    for file in OUTPUT_DIR.glob("*.csv"):
        print(f"- {file}")


if __name__ == "__main__":
    main()

