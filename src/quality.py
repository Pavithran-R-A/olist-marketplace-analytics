from __future__ import annotations

import json

import pandas as pd

from .common import connection, csv_files
from .config import DB_PATH, REPORTS

EXPECTED_FILES = {
    "olist_customers_dataset.csv", "olist_geolocation_dataset.csv", "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv", "olist_order_reviews_dataset.csv", "olist_orders_dataset.csv",
    "olist_products_dataset.csv", "olist_sellers_dataset.csv", "product_category_name_translation.csv",
}


def _row(name: str, severity: str, observed: object, expected: str, status: str, implication: str) -> dict[str, object]:
    return {"rule_name": name, "severity": severity, "observed_value": observed,
            "expected_condition": expected, "status": status, "business_implication": implication}


def run_quality_gate(raise_on_critical: bool = True) -> list[dict[str, object]]:
    files = {p.name for p in csv_files()}
    rows: list[dict[str, object]] = [_row("source_file_completeness", "critical", len(files), f"all {len(EXPECTED_FILES)} expected files", "PASS" if EXPECTED_FILES <= files else "FAIL", "Missing source files invalidate the model.")]
    frames: dict[str, pd.DataFrame] = {}
    for name in ["olist_customers_dataset.csv", "olist_orders_dataset.csv", "olist_order_items_dataset.csv", "olist_order_payments_dataset.csv", "olist_order_reviews_dataset.csv", "olist_products_dataset.csv", "olist_sellers_dataset.csv"]:
        if name in files:
            frames[name] = pd.read_csv(next(p for p in csv_files() if p.name == name))
    checks = [
        ("customer_key_uniqueness", "critical", frames.get("olist_customers_dataset.csv"), "customer_id", "Customer identity joins must be one-to-one."),
        ("order_key_uniqueness", "critical", frames.get("olist_orders_dataset.csv"), "order_id", "Orders must have one source row."),
        ("item_grain_uniqueness", "critical", frames.get("olist_order_items_dataset.csv"), ["order_id", "order_item_id"], "Item grain must not duplicate."),
        ("seller_key_uniqueness", "warn", frames.get("olist_sellers_dataset.csv"), "seller_id", "Seller joins should remain stable."),
        ("product_key_uniqueness", "warn", frames.get("olist_products_dataset.csv"), "product_id", "Product joins should remain stable."),
    ]
    for name, severity, frame, key, implication in checks:
        if frame is None:
            continue
        dupes = int(frame.duplicated(key).sum())
        rows.append(_row(name, severity, dupes, "0 duplicates", "PASS" if dupes == 0 else ("FAIL" if severity == "critical" else "WARN"), implication))
    orders, items = frames.get("olist_orders_dataset.csv"), frames.get("olist_order_items_dataset.csv")
    if orders is not None and items is not None:
        order_ids = set(orders.order_id)
        orphan = int((~items.order_id.isin(order_ids)).sum())
        rows.append(_row("orphan_item_order_ids", "critical", orphan, "0 orphan IDs", "PASS" if orphan == 0 else "FAIL", "Orphan items distort GMV."))
        products, sellers = frames.get("olist_products_dataset.csv"), frames.get("olist_sellers_dataset.csv")
        if products is not None:
            orphan_products = int((~items.product_id.isin(set(products.product_id))).sum())
            rows.append(_row("orphan_item_product_ids", "critical", orphan_products, "0 orphan IDs", "PASS" if orphan_products == 0 else "FAIL", "Product joins drive category analysis."))
        if sellers is not None:
            orphan_sellers = int((~items.seller_id.isin(set(sellers.seller_id))).sum())
            rows.append(_row("orphan_item_seller_ids", "critical", orphan_sellers, "0 orphan IDs", "PASS" if orphan_sellers == 0 else "FAIL", "Seller joins drive fulfillment analysis."))
        payments = frames.get("olist_order_payments_dataset.csv")
        reviews = frames.get("olist_order_reviews_dataset.csv")
        if payments is not None:
            orphan_payments = int((~payments.order_id.isin(order_ids)).sum())
            rows.append(_row("orphan_payment_order_ids", "warn", orphan_payments, "0 preferred", "PASS" if orphan_payments == 0 else "WARN", "Payment reconciliation requires matching orders."))
            negative_payments = int((payments.payment_value < 0).sum())
            rows.append(_row("negative_payment_value", "critical", negative_payments, "0 rows", "PASS" if negative_payments == 0 else "FAIL", "Payment quality affects reconciliation."))
        if reviews is not None:
            orphan_reviews = int((~reviews.order_id.isin(order_ids)).sum())
            rows.append(_row("orphan_review_order_ids", "warn", orphan_reviews, "0 preferred", "PASS" if orphan_reviews == 0 else "WARN", "Review joins affect satisfaction coverage."))
        missing_customer = int(orders.customer_id.isna().sum())
        rows.append(_row("missing_order_customer_ids", "critical", missing_customer, "0 missing IDs", "PASS" if missing_customer == 0 else "FAIL", "Customer analysis requires identity."))
        purchase = pd.to_datetime(orders.order_purchase_timestamp, errors="coerce")
        delivered = pd.to_datetime(orders.order_delivered_customer_date, errors="coerce")
        estimated = pd.to_datetime(orders.order_estimated_delivery_date, errors="coerce")
        early = int((delivered < purchase).fillna(False).sum())
        rows.append(_row("delivery_before_purchase", "critical", early, "0 rows", "PASS" if early == 0 else "FAIL", "Negative delivery duration is invalid."))
        missing_delivered = int((orders.order_status.eq("delivered") & delivered.isna()).sum())
        rows.append(_row("delivered_missing_timestamp", "warn", missing_delivered, "0 preferred", "PASS" if missing_delivered == 0 else "WARN", "Delivery KPIs exclude these rows."))
        inconsistent_estimate = int(((estimated < purchase).fillna(False)).sum())
        rows.append(_row("estimated_date_before_purchase", "warn", inconsistent_estimate, "0 rows", "PASS" if inconsistent_estimate == 0 else "WARN", "Promise dates may be unreliable."))
        valid_status = {"delivered", "shipped", "canceled", "unavailable", "invoiced", "processing", "created", "approved"}
        bad_status = int((~orders.order_status.isin(valid_status)).sum())
        rows.append(_row("invalid_order_status", "critical", bad_status, "0 rows", "PASS" if bad_status == 0 else "FAIL", "Status logic drives all rate metrics."))
    if items is not None:
        for col in ["price", "freight_value"]:
            bad = int((items[col] < 0).sum())
            rows.append(_row(f"negative_{col}", "critical", bad, "0 rows", "PASS" if bad == 0 else "FAIL", "Negative monetary values invalidate GMV."))
    reviews = frames.get("olist_order_reviews_dataset.csv")
    if reviews is not None:
        bad = int((~reviews.review_score.between(1, 5)).sum())
        rows.append(_row("review_score_bounds", "critical", bad, "0 rows outside 1-5", "PASS" if bad == 0 else "FAIL", "Review comparisons require valid scores."))
    if DB_PATH.exists():
        con = connection()
        model_orders, source_orders = con.sql("SELECT COUNT(*), (SELECT COUNT(*) FROM raw_orders) FROM fact_orders").fetchone()
        rows.append(_row("source_order_reconciliation", "critical", model_orders, f"{source_orders} modeled orders", "PASS" if model_orders == source_orders else "FAIL", "Order counts must reconcile."))
        model_gmv, source_gmv = con.sql("SELECT SUM(gmv), (SELECT SUM(price) FROM raw_order_items) FROM fact_orders").fetchone()
        rows.append(_row("gmv_reconciliation", "critical", float(model_gmv), f"source {float(source_gmv):.2f}", "PASS" if abs(model_gmv - source_gmv) < 0.01 else "FAIL", "Fanout must not inflate GMV."))
        fact_dupes = con.sql("SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM fact_orders").fetchone()[0]
        rows.append(_row("fact_orders_uniqueness", "critical", fact_dupes, "0 duplicate order IDs", "PASS" if fact_dupes == 0 else "FAIL", "Order fact must retain its declared grain."))
        con.close()
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "quality_gate.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    failures = [r for r in rows if r["status"] == "FAIL" and r["severity"] == "critical"]
    if failures and raise_on_critical:
        raise ValueError(f"Critical data-quality failures: {[r['rule_name'] for r in failures]}")
    return rows
