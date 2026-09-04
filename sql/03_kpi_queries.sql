-- Monthly marketplace GMV and order trend.
WITH monthly AS (
  SELECT date_trunc('month', purchase_ts) month, SUM(gmv) gmv, COUNT(*) orders
  FROM fact_orders GROUP BY 1
)
SELECT month, gmv, orders, gmv / NULLIF(orders, 0) AS aov,
  (gmv / NULLIF(orders, 0)) / NULLIF(LAG(gmv / NULLIF(orders, 0)) OVER (ORDER BY month), 0) - 1 AS aov_mom
FROM monthly ORDER BY month;

