-- DuckDB model is created by src.transform.
-- fact_orders: one row per order; GMV and freight pre-aggregated from items.
-- fact_order_items: one row per order-item-seller combination.
-- fact_payments: one row per payment installment/sequence.
-- Reviews are pre-aggregated to order grain in fact_orders.

