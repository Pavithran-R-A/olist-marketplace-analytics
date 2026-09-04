import pandas as pd

from src.metrics import add_delivery_flags


def test_negative_monetary_values_are_detected():
    frame = pd.DataFrame({"price": [10.0, -1.0], "freight_value": [2.0, 1.0]})
    assert int((frame["price"] < 0).sum()) == 1


def test_delivery_before_purchase_is_not_valid():
    frame = pd.DataFrame({
        "order_status": ["delivered"],
        "order_purchase_timestamp": ["2020-01-05"],
        "order_delivered_customer_date": ["2020-01-04"],
        "order_estimated_delivery_date": ["2020-01-06"],
    })
    result = add_delivery_flags(frame)
    assert result["delivery_days"].iloc[0] < 0

