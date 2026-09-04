WITH purchases AS (
  SELECT customer_unique_id, COUNT(*) frequency, SUM(gmv) monetary,
    MIN(purchase_ts) first_purchase, MAX(purchase_ts) last_purchase
  FROM fact_orders GROUP BY 1
)
SELECT *, CASE WHEN frequency > 1 THEN TRUE ELSE FALSE END AS is_repeat
FROM purchases;

