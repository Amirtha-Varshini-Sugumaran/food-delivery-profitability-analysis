"""Train a simple repeat-order prediction model.

This is intentionally explainable and lightweight. It is a Data Analyst style
model, used to support retention prioritisation rather than automated decisions.

Run from the project root:
    python scripts/04_repeat_order_model.py
"""

from pathlib import Path

import pandas as pd

try:
    from sklearn.compose import ColumnTransformer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report, roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    SKLEARN_AVAILABLE = True
except ModuleNotFoundError:
    SKLEARN_AVAILABLE = False


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "food_delivery_cleaned.csv"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    features = [
        "city",
        "cuisine_type",
        "payment_method",
        "customer_tenure_group",
        "acquisition_channel",
        "discount_band",
        "weather_condition",
        "delivery_delay_flag",
        "order_value",
        "discount_amount",
        "gross_profit",
        "profit_margin_pct",
        "rating",
        "distance_km",
        "weekend_flag",
        "festival_flag",
    ]

    if not SKLEARN_AVAILABLE:
        # Lightweight fallback for environments without scikit-learn. It is not a
        # replacement for the notebook model, but it keeps the script runnable.
        segment_rates = df.groupby("customer_tenure_group")["repeat_customer_flag"].mean()
        discount_rates = df.groupby("discount_band")["repeat_customer_flag"].mean()
        base_rate = df["repeat_customer_flag"].mean()
        scored = df.copy()
        scored["repeat_score"] = (
            0.55 * scored["customer_tenure_group"].map(segment_rates)
            + 0.25 * scored["discount_band"].map(discount_rates)
            + 0.10 * (scored["rating"] / 5)
            + 0.10 * (1 - scored["delivery_delay_flag"])
        )
        scored["predicted_repeat_flag"] = (scored["repeat_score"] >= base_rate).astype(int)
        accuracy = (scored["predicted_repeat_flag"] == scored["repeat_customer_flag"]).mean()
        print("scikit-learn is not installed, so a simple analyst scorecard was used.")
        print(f"Baseline repeat rate: {base_rate:.2%}")
        print(f"Scorecard accuracy: {accuracy:.2%}")
        print("Top score drivers: tenure group, discount band, rating, and delivery delay flag.")
        return

    X = df[features]
    y = df["repeat_customer_flag"]
    categorical = X.select_dtypes(include="object").columns.tolist()
    numeric = [col for col in X.columns if col not in categorical]
    preprocess = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", StandardScaler(), numeric),
        ]
    )
    model = Pipeline(
        [
            ("preprocess", preprocess),
            ("model", LogisticRegression(max_iter=1000)),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, predictions))
    print(f"ROC AUC: {roc_auc_score(y_test, probabilities):.3f}")


if __name__ == "__main__":
    main()
