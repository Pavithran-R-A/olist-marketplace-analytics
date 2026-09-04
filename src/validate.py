from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pandas as pd

from .common import csv_files
from .config import REPORTS
from .quality import run_quality_gate


def profile_file(path: Path) -> dict[str, object]:
    con = duckdb.connect()
    columns = [row[0] for row in con.sql("SELECT column_name FROM (DESCRIBE SELECT * FROM read_csv_auto(?))", params=[str(path)]).fetchall()]
    quoted = ", ".join('"' + name.replace('"', '""') + '"' for name in columns)
    missing = " + ".join(f"CASE WHEN \"{name.replace(chr(34), chr(34) * 2)}\" IS NULL THEN 1 ELSE 0 END" for name in columns)
    row = con.sql(f"SELECT COUNT(*) AS row_count, COUNT(DISTINCT ({quoted})) AS distinct_rows, SUM({missing}) AS missing_values FROM read_csv_auto(?)", params=[str(path)]).fetchone()
    con.close()
    return {
        "filename": path.name,
        "rows": int(row[0]),
        "columns": len(columns),
        "duplicate_rows": int(row[0] - row[1]),
        "missing_values": int(row[2] or 0),
        "columns_list": columns,
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
    run_quality_gate()
    print(json.dumps(profiles, indent=2))
    return profiles


if __name__ == "__main__":
    validate()
