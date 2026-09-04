-- Source quality rules used by the validation report.
SELECT order_status, COUNT(*) AS orders FROM raw_orders GROUP BY 1 ORDER BY 1;
SELECT COUNT(*) AS delivery_before_purchase
FROM raw_orders
WHERE order_delivered_customer_date < order_purchase_timestamp;
SELECT COUNT(*) AS negative_prices FROM raw_order_items WHERE price < 0;

