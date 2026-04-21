"""End-to-end food delivery profitability analysis.

This script is the main Python analysis file for the portfolio project.

It covers:
- KPI analysis
- profitability analysis
- discount and retention analysis
- delivery performance analysis
- statistical checks
- customer segmentation
- a lightweight repeat-order prediction scorecard
- chart exports

Run from the project root:
    python scripts/05_full_python_analysis.py
"""

from __future__ import annotations

from math import erf, sqrt
from pathlib import Path

import pandas as pd

try:
    import matplotlib.pyplot as plt

    MATPLOTLIB_AVAILABLE = True
except ModuleNotFoundError:
    MATPLOTLIB_AVAILABLE = False


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "food_delivery_cleaned.csv"
OUTPUT_DIR = ROOT / "artifacts" / "python_analysis"
FIGURE_DIR = OUTPUT_DIR / "figures"
REPORT_PATH = OUTPUT_DIR / "python_analysis_summary.md"


def normal_cdf(value: float) -> float:
    return 0.5 * (1 + erf(value / sqrt(2)))


def approximate_two_sample_p_value(group_a: pd.Series, group_b: pd.Series) -> float:
    mean_diff = group_a.mean() - group_b.mean()
    standard_error = sqrt(
        group_a.var(ddof=1) / len(group_a) + group_b.var(ddof=1) / len(group_b)
    )
    z_score = abs(mean_diff / standard_error)
    return 2 * (1 - normal_cdf(z_score))


def save_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str, filename: str) -> None:
    if not MATPLOTLIB_AVAILABLE:
        return
    plt.figure(figsize=(10, 5))
    plt.bar(data[x_col].astype(str), data[y_col])
    plt.title(title)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / filename, dpi=140)
    plt.close()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH, parse_dates=["order_datetime"])

    kpis = {
        "total_orders": len(df),
        "gross_profit": round(df["gross_profit"].sum(), 2),
        "average_order_value": round(df["order_value"].mean(), 2),
        "average_margin_pct": round(df["profit_margin_pct"].mean(), 2),
        "repeat_rate_pct": round(df["repeat_customer_flag"].mean() * 100, 2),
        "delay_rate_pct": round(df["delivery_delay_flag"].mean() * 100, 2),
        "average_rating": round(df["rating"].mean(), 2),
        "total_discount": round(df["discount_amount"].sum(), 2),
    }

    city_summary = (
        df.groupby("city")
        .agg(
            orders=("order_id", "count"),
            gross_profit=("gross_profit", "sum"),
            avg_margin_pct=("profit_margin_pct", "mean"),
            repeat_rate_pct=("repeat_customer_flag", lambda x: x.mean() * 100),
            delay_rate_pct=("delivery_delay_flag", lambda x: x.mean() * 100),
            avg_rating=("rating", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("gross_profit", ascending=False)
    )

    discount_summary = (
        df.groupby("discount_band", observed=True)
        .agg(
            orders=("order_id", "count"),
            avg_discount=("discount_amount", "mean"),
            avg_profit=("gross_profit", "mean"),
            repeat_rate_pct=("repeat_customer_flag", lambda x: x.mean() * 100),
            avg_rating=("rating", "mean"),
        )
        .round(2)
        .reset_index()
    )

    zone_risk = (
        df.groupby(["city", "zone"])
        .agg(
            orders=("order_id", "count"),
            delay_rate_pct=("delivery_delay_flag", lambda x: x.mean() * 100),
            avg_delay_minutes=("delay_minutes", "mean"),
            avg_rating=("rating", "mean"),
            gross_profit=("gross_profit", "sum"),
        )
        .query("orders >= 30")
        .round(2)
        .reset_index()
        .sort_values(["delay_rate_pct", "avg_rating"], ascending=[False, True])
    )

    customer_summary = (
        df.groupby("customer_id")
        .agg(
            orders=("order_id", "count"),
            total_profit=("gross_profit", "sum"),
            avg_margin_pct=("profit_margin_pct", "mean"),
            avg_discount=("discount_amount", "mean"),
            delay_rate=("delivery_delay_flag", "mean"),
            avg_rating=("rating", "mean"),
            repeat_rate=("repeat_customer_flag", "mean"),
        )
        .reset_index()
    )
    customer_summary["profit_quartile"] = pd.qcut(
        customer_summary["total_profit"], 4, labels=[1, 2, 3, 4]
    )
    customer_summary["frequency_quartile"] = pd.qcut(
        customer_summary["orders"].rank(method="first"), 4, labels=[1, 2, 3, 4]
    )

    def segment(row: pd.Series) -> str:
        if row["profit_quartile"] == 4 and row["frequency_quartile"] >= 3:
            return "High-value loyal"
        if row["profit_quartile"] <= 2 and row["frequency_quartile"] == 4:
            return "High-volume low-margin"
        if row["profit_quartile"] == 4:
            return "High-profit occasional"
        return "Standard"

    customer_summary["customer_segment"] = customer_summary.apply(segment, axis=1)
    segment_summary = (
        customer_summary.groupby("customer_segment")
        .agg(
            customers=("customer_id", "count"),
            avg_orders=("orders", "mean"),
            avg_profit=("total_profit", "mean"),
            avg_margin_pct=("avg_margin_pct", "mean"),
            avg_rating=("avg_rating", "mean"),
        )
        .round(2)
        .reset_index()
        .sort_values("avg_profit", ascending=False)
    )

    delayed = df.loc[df["delivery_delay_flag"] == 1, "rating"]
    on_time = df.loc[df["delivery_delay_flag"] == 0, "rating"]
    delay_rating_p = approximate_two_sample_p_value(delayed, on_time)

    tenure_repeat = df.groupby("customer_tenure_group")["repeat_customer_flag"].mean()
    discount_repeat = df.groupby("discount_band", observed=True)["repeat_customer_flag"].mean()

    # Lightweight repeat-order scorecard for analyst-friendly model explanation.
    base_repeat_rate = df["repeat_customer_flag"].mean()
    scored = df.copy()
    scored["repeat_score"] = (
        0.50 * scored["customer_tenure_group"].map(tenure_repeat)
        + 0.25 * scored["discount_band"].map(discount_repeat)
        + 0.15 * (scored["rating"] / 5)
        + 0.10 * (1 - scored["delivery_delay_flag"])
    )
    scored["predicted_repeat_flag"] = (scored["repeat_score"] >= base_repeat_rate).astype(int)
    scorecard_accuracy = (
        scored["predicted_repeat_flag"] == scored["repeat_customer_flag"]
    ).mean()

    city_summary.to_csv(OUTPUT_DIR / "city_profitability_summary.csv", index=False)
    discount_summary.to_csv(OUTPUT_DIR / "discount_retention_summary.csv", index=False)
    zone_risk.head(20).to_csv(OUTPUT_DIR / "top_zone_risk_summary.csv", index=False)
    segment_summary.to_csv(OUTPUT_DIR / "customer_segment_summary.csv", index=False)
    scored[
        [
            "order_id",
            "customer_id",
            "customer_tenure_group",
            "rating",
            "discount_band",
            "delivery_delay_flag",
            "repeat_score",
            "predicted_repeat_flag",
            "repeat_customer_flag",
        ]
    ].head(500).to_csv(OUTPUT_DIR / "repeat_score_sample.csv", index=False)

    save_bar_chart(
        city_summary,
        "city",
        "gross_profit",
        "Gross Profit by City",
        "gross_profit_by_city.png",
    )
    save_bar_chart(
        discount_summary,
        "discount_band",
        "repeat_rate_pct",
        "Repeat Rate by Discount Band",
        "repeat_rate_by_discount_band.png",
    )
    save_bar_chart(
        zone_risk.head(10).assign(city_zone=lambda x: x["city"] + " - " + x["zone"]),
        "city_zone",
        "delay_rate_pct",
        "Top Delay Hotspots",
        "top_delay_hotspots.png",
    )

    chart_note = (
        "Chart PNGs were created in `artifacts/python_analysis/figures/`."
        if MATPLOTLIB_AVAILABLE
        else "Chart PNGs were skipped because matplotlib is not installed in this local runtime. The CSV outputs are still created and can be charted in Power BI or Excel."
    )

    report = f"""# Python Analysis Summary

## KPI Snapshot

| KPI | Value |
|---|---:|
| Total Orders | {kpis["total_orders"]:,} |
| Gross Profit | INR {kpis["gross_profit"]:,.2f} |
| Average Order Value | INR {kpis["average_order_value"]:,.2f} |
| Average Margin % | {kpis["average_margin_pct"]:.2f}% |
| Repeat Rate % | {kpis["repeat_rate_pct"]:.2f}% |
| Delay Rate % | {kpis["delay_rate_pct"]:.2f}% |
| Average Rating | {kpis["average_rating"]:.2f} |
| Total Discount | INR {kpis["total_discount"]:,.2f} |

## Main Findings

- Highest-profit cities are not automatically the cleanest operational markets. Profit needs to be reviewed with delay rate and rating.
- Discount bands show different repeat behaviour, but the repeat lift should be compared against margin loss.
- Delayed orders have a lower average rating than on-time orders.
- The approximate p-value for the delayed vs on-time rating difference is {delay_rating_p:.6f}, which supports treating delay as a customer experience issue.
- Customer segmentation separates high-value loyal customers from high-volume low-margin customers.
- The repeat-order scorecard accuracy is {scorecard_accuracy:.2%}. It is useful for prioritisation, not automated decision-making.

## Chart Output

{chart_note}

## Files Created By This Script

- `artifacts/python_analysis/city_profitability_summary.csv`
- `artifacts/python_analysis/discount_retention_summary.csv`
- `artifacts/python_analysis/top_zone_risk_summary.csv`
- `artifacts/python_analysis/customer_segment_summary.csv`
- `artifacts/python_analysis/repeat_score_sample.csv`
- `artifacts/python_analysis/figures/gross_profit_by_city.png`
- `artifacts/python_analysis/figures/repeat_rate_by_discount_band.png`
- `artifacts/python_analysis/figures/top_delay_hotspots.png`
"""
    REPORT_PATH.write_text(report, encoding="utf-8")

    print("Python analysis complete.")
    print(f"Summary report: {REPORT_PATH}")
    print(chart_note)


if __name__ == "__main__":
    main()
