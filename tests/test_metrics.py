import pandas as pd
import pytest

from src.metrics import add_delivery_flags, calculate_kpis, rfm_segment


def test_kpis_reconcile_order_and_gmv_totals():
    orders = pd.DataFrame({
        "order_id": ["o1", "o2", "o3"],
        "customer_unique_id": ["c1", "c2", "c1"],
        "order_status": ["delivered", "canceled", "delivered"],
        "gmv": [10.0, 20.0, 15.0],
    })
    result = calculate_kpis(orders)
    assert result["orders"] == 3
    assert result["gmv"] == pytest.approx(45.0)
    assert result["cancelled_orders"] == 1
    assert result["repeat_customers"] == 1


def test_delivery_flag_requires_delivered_order_and_compares_dates():
    frame = pd.DataFrame({
        "order_status": ["delivered", "delivered", "canceled"],
        "order_delivered_customer_date": pd.to_datetime(["2020-01-05", "2020-01-03", None]),
        "order_estimated_delivery_date": pd.to_datetime(["2020-01-04", "2020-01-04", "2020-01-03"]),
    })
    result = add_delivery_flags(frame)
    assert result["is_late"].tolist() == [True, False, False]


def test_rfm_segment_labels_high_value_customer():
    assert rfm_segment(recency=5, frequency=8, monetary=900) == "Champions"

