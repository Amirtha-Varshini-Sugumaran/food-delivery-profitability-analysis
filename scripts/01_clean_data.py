"""Clean the raw food delivery dataset and rebuild the processed CSV.

Run from the project root:
    python scripts/01_clean_data.py
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "food_delivery_raw.csv"
CLEAN_PATH = ROOT / "data" / "processed" / "food_delivery_cleaned.csv"


def normalise_city(value: object) -> str:
    city = str(value).strip().title()
    return {"Delhi-Ncr": "Delhi NCR", "Delhi Ncr": "Delhi NCR"}.get(city, city)


def main() -> None:
    raw = pd.read_csv(RAW_PATH)
    df = raw.copy()

    df["city"] = df["city"].apply(normalise_city)
    for col in ["zone", "cuisine_type", "payment_method", "weather_condition"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.title()
            .replace({"": "Unknown", "Nan": "Unknown"})
        )

    df["order_datetime"] = pd.to_datetime(
        df["order_datetime"], errors="coerce", dayfirst=True
    )
    df = df.drop_duplicates(subset="order_id", keep="last")

    df["delivery_partner_id"] = (
        df["delivery_partner_id"].fillna("UNASSIGNED").replace("", "UNASSIGNED")
    )
    df["discount_amount"] = pd.to_numeric(
        df["discount_amount"], errors="coerce"
    ).fillna(0)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["rating"] = df["rating"].fillna(df["rating"].median())

    numeric_cols = [
        "delivery_time_minutes",
        "promised_delivery_time_minutes",
        "order_value",
        "delivery_fee",
        "packaging_charge",
        "platform_commission",
        "refund_amount",
        "distance_km",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["delivery_time_minutes"] = df["delivery_time_minutes"].clip(lower=10, upper=180)
    df["delivery_delay_flag"] = (
        df["delivery_time_minutes"] > df["promised_delivery_time_minutes"]
    ).astype(int)
    df["gross_profit"] = (
        df["platform_commission"]
        + df["delivery_fee"]
        + df["packaging_charge"]
        - df["discount_amount"]
        - df["refund_amount"]
    ).round(2)
    df["profit_margin_pct"] = (df["gross_profit"] / df["order_value"] * 100).round(2)
    df["delay_minutes"] = (
        df["delivery_time_minutes"] - df["promised_delivery_time_minutes"]
    ).clip(lower=0)
    df["discount_rate"] = df["discount_amount"] / df["order_value"]
    df["discount_band"] = pd.cut(
        df["discount_rate"],
        bins=[-0.01, 0, 0.10, 0.20, 1],
        labels=["No Discount", "Low", "Medium", "High"],
    )
    df["order_month"] = df["order_datetime"].dt.to_period("M").astype(str)
    df = df.drop(columns=["discount_rate"])

    df.to_csv(CLEAN_PATH, index=False)
    print(f"Raw rows: {len(raw):,}")
    print(f"Cleaned rows: {len(df):,}")
    print(f"Duplicate orders removed: {raw.duplicated('order_id').sum():,}")
    print(f"Saved: {CLEAN_PATH}")


if __name__ == "__main__":
    main()

