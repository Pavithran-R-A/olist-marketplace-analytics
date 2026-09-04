SELECT order_status, COUNT(*) orders, SUM(gmv) gmv,
  COUNT(*) * 1.0 / SUM(COUNT(*)) OVER () AS order_share
FROM fact_orders GROUP BY 1 ORDER BY orders DESC;

