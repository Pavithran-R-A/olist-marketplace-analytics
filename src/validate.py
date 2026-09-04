from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .common import csv_files
from .config import REPORTS


def profile_file(path: Path) -> dict[str, object]:
    frame = pd.read_csv(path)
    return {
        "filename": path.name,
        "rows": len(frame),
        "columns": len(frame.columns),
        "duplicate_rows": int(frame.duplicated().sum()),
        "missing_values": int(frame.isna().sum().sum()),
        "columns_list": list(frame.columns),
    }


def validate() -> list[dict[str, object]]:
    REPORTS.mkdir(parents=True, exist_ok=True)
    profiles = [profile_file(path) for path in csv_files()]
    (REPORTS / "source_profile.json").write_text(json.dumps(profiles, indent=2), encoding="utf-8")
    if profiles:
        pd.DataFrame(profiles).to_csv(REPORTS / "source_profile.csv", index=False)
    by_name = {p.name: p for p in csv_files()}
    rules: dict[str, int] = {}
    if "olist_orders_dataset.csv" in by_name:
        orders = pd.read_csv(by_name["olist_orders_dataset.csv"], parse_dates=["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"])
        rules["orders_duplicate_keys"] = int(orders.order_id.duplicated().sum())
        rules["delivery_before_purchase"] = int((orders.order_delivered_customer_date < orders.order_purchase_timestamp).fillna(False).sum())
        rules["delivered_without_delivery_timestamp"] = int((orders.order_status.eq("delivered") & orders.order_delivered_customer_date.isna()).sum())
    if "olist_order_items_dataset.csv" in by_name:
        items = pd.read_csv(by_name["olist_order_items_dataset.csv"])
        rules["negative_price"] = int((items.price < 0).sum())
        rules["negative_freight"] = int((items.freight_value < 0).sum())
    if "olist_order_reviews_dataset.csv" in by_name:
        reviews = pd.read_csv(by_name["olist_order_reviews_dataset.csv"])
        rules["duplicate_review_order_pairs"] = int(reviews.duplicated(["review_id", "order_id"]).sum())
    (REPORTS / "quality_rules.json").write_text(json.dumps(rules, indent=2), encoding="utf-8")
    print(json.dumps(profiles, indent=2))
    return profiles


if __name__ == "__main__":
    validate()
