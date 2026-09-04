from __future__ import annotations

import pandas as pd


def add_delivery_flags(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with defensible delivery duration and lateness fields."""
    result = frame.copy()
    delivered = pd.to_datetime(result["order_delivered_customer_date"], errors="coerce")
    estimated = pd.to_datetime(result["order_estimated_delivery_date"], errors="coerce")
    result["delivery_days"] = (delivered - pd.to_datetime(result.get("order_purchase_timestamp"), errors="coerce")).dt.total_seconds() / 86400
    result["is_late"] = result["order_status"].eq("delivered") & delivered.notna() & estimated.notna() & (delivered > estimated)
    return result


def calculate_kpis(orders: pd.DataFrame) -> dict[str, float | int]:
    """Calculate order-level KPIs without item/payment fanout."""
    customer_counts = orders.groupby("customer_unique_id")["order_id"].nunique()
    return {
        "orders": int(orders["order_id"].nunique()),
        "gmv": float(orders["gmv"].sum()),
        "delivered_orders": int(orders["order_status"].eq("delivered").sum()),
        "cancelled_orders": int(orders["order_status"].eq("canceled").sum()),
        "repeat_customers": int((customer_counts > 1).sum()),
        "customers": int(customer_counts.size),
    }


def rfm_segment(recency: float, frequency: float, monetary: float) -> str:
    if recency <= 30 and frequency >= 5 and monetary >= 500:
        return "Champions"
    if frequency >= 2 and monetary >= 250:
        return "Loyal customers"
    if recency <= 90:
        return "Recent customers"
    return "At risk"

