SELECT customer_state, COUNT(*) orders, SUM(gmv) gmv,
  AVG(CASE WHEN is_late THEN 1 ELSE 0 END) late_rate,
  AVG(review_score) avg_review
FROM fact_orders GROUP BY 1 ORDER BY gmv DESC;

