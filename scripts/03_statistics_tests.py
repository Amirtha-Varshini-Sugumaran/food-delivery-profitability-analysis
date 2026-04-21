"""Run practical statistical checks used in the project narrative.

Run from the project root:
    python scripts/03_statistics_tests.py
"""

from math import erf, sqrt
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "food_delivery_cleaned.csv"


def normal_cdf(value: float) -> float:
    return 0.5 * (1 + erf(value / sqrt(2)))


def approximate_two_sample_p_value(group_a: pd.Series, group_b: pd.Series) -> float:
    """Return a normal-approximation p-value for a two-sample mean difference.

    This keeps the script runnable in lightweight environments where scipy is not
    installed. The notebook can still use scipy when available.
    """
    mean_diff = group_a.mean() - group_b.mean()
    standard_error = sqrt(group_a.var(ddof=1) / len(group_a) + group_b.var(ddof=1) / len(group_b))
    z_score = abs(mean_diff / standard_error)
    return 2 * (1 - normal_cdf(z_score))


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    delayed = df.loc[df["delivery_delay_flag"] == 1, "rating"]
    on_time = df.loc[df["delivery_delay_flag"] == 0, "rating"]
    rating_p_value = approximate_two_sample_p_value(delayed, on_time)

    repeat_by_discount = df.groupby("discount_band")["repeat_customer_flag"].mean()
    repeat_spread = repeat_by_discount.max() - repeat_by_discount.min()

    tenure_profit = df.groupby("customer_tenure_group")["gross_profit"].mean()
    tenure_profit_spread = tenure_profit.max() - tenure_profit.min()

    print("Delayed vs on-time ratings")
    print(f"- Delayed average rating: {delayed.mean():.2f}")
    print(f"- On-time average rating: {on_time.mean():.2f}")
    print(f"- Difference: {on_time.mean() - delayed.mean():.2f}")
    print(f"- approximate p-value: {rating_p_value:.6f}")
    print()
    print("Discount band and repeat behaviour")
    print(f"- Repeat rate spread across discount bands: {repeat_spread:.2%}")
    print("- Business read: compare this spread against the margin lost to discounts.")
    print()
    print("Profitability difference by tenure group")
    print(f"- Average profit spread across tenure groups: INR {tenure_profit_spread:.2f}")


if __name__ == "__main__":
    main()
