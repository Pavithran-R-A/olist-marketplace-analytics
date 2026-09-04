-- Executable business outputs. Run after src.transform.
CREATE OR REPLACE TABLE monthly_kpis AS
WITH m AS (
  SELECT date_trunc('month', purchase_ts) AS month, SUM(gmv) AS gmv,
    COUNT(*) AS orders, AVG(gmv) AS aov
  FROM fact_orders GROUP BY 1
)
SELECT *, gmv / NULLIF(LAG(gmv) OVER (ORDER BY month), 0) - 1 AS gmv_mom,
  orders * 1.0 / NULLIF(LAG(orders) OVER (ORDER BY month), 0) - 1 AS orders_mom,
  SUM(gmv) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_gmv
FROM m ORDER BY month;

CREATE OR REPLACE TABLE status_kpis AS
SELECT order_status, COUNT(*) AS orders, SUM(gmv) AS gmv,
  COUNT(*) * 1.0 / SUM(COUNT(*)) OVER () AS order_share
FROM fact_orders GROUP BY 1 ORDER BY orders DESC;

CREATE OR REPLACE TABLE category_kpis AS
WITH c AS (
  SELECT category, SUM(price) AS gmv, COUNT(DISTINCT order_id) AS orders,
    COUNT(*) AS items, SUM(freight_value) AS freight
  FROM fact_order_items GROUP BY 1
)
SELECT *, gmv / NULLIF(orders, 0) AS aov,
  freight / NULLIF(gmv, 0) AS freight_to_gmv,
  SUM(gmv) OVER (ORDER BY gmv DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    / NULLIF(SUM(gmv) OVER (), 0) AS cumulative_gmv_share,
  RANK() OVER (ORDER BY gmv DESC) AS gmv_rank
FROM c ORDER BY gmv DESC;

CREATE OR REPLACE TABLE state_kpis AS
SELECT customer_state AS state, COUNT(*) AS orders, SUM(gmv) AS gmv,
  AVG(CASE WHEN order_status='delivered' THEN is_late::INT END) AS late_rate,
  AVG(CASE WHEN order_status='delivered' THEN delivery_days END) AS avg_delivery_days,
  MEDIAN(CASE WHEN order_status='delivered' THEN delivery_days END) AS median_delivery_days,
  AVG(review_score) AS avg_review, SUM(freight_value) AS freight,
  SUM(freight_value) / NULLIF(SUM(gmv), 0) AS freight_to_gmv
FROM fact_orders GROUP BY 1 ORDER BY gmv DESC;

CREATE OR REPLACE TABLE seller_kpis AS
WITH s AS (
  SELECT oi.seller_id, COUNT(DISTINCT oi.order_id) AS orders, SUM(oi.price) AS gmv,
    SUM(oi.freight_value) AS freight,
    AVG(CASE WHEN fo.order_status='delivered' THEN fo.is_late::INT END) AS late_rate,
    AVG(CASE WHEN fo.order_status='delivered' THEN fo.delivery_days END) AS avg_delivery_days,
    MEDIAN(CASE WHEN fo.order_status='delivered' THEN fo.delivery_days END) AS median_delivery_days,
    AVG(fo.review_score) AS avg_review
  FROM fact_order_items oi JOIN fact_orders fo USING(order_id)
  GROUP BY oi.seller_id
)
SELECT *, freight / NULLIF(gmv, 0) AS freight_to_gmv,
  gmv / NULLIF(SUM(gmv) OVER (), 0) AS gmv_share,
  SUM(gmv) OVER (ORDER BY gmv DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    / NULLIF(SUM(gmv) OVER (), 0) AS cumulative_gmv_share,
  RANK() OVER (ORDER BY late_rate DESC) AS late_rank
FROM s WHERE orders >= 20 ORDER BY late_rate DESC, orders DESC, seller_id;

CREATE OR REPLACE TABLE fulfillment_category AS
SELECT oi.category, COUNT(DISTINCT oi.order_id) AS orders, SUM(oi.price) AS gmv,
  AVG(CASE WHEN fo.order_status='delivered' THEN fo.is_late::INT END) AS late_rate,
  AVG(CASE WHEN fo.order_status='delivered' THEN fo.delivery_days END) AS avg_delivery_days,
  MEDIAN(CASE WHEN fo.order_status='delivered' THEN fo.delivery_days END) AS median_delivery_days,
  AVG(fo.review_score) AS avg_review
FROM fact_order_items oi JOIN fact_orders fo USING(order_id)
GROUP BY 1 HAVING COUNT(DISTINCT oi.order_id) >= 100 ORDER BY late_rate DESC;

CREATE OR REPLACE TABLE freight_state AS
WITH state_totals AS (
  SELECT customer_state AS state, COUNT(*) AS orders, SUM(gmv) AS gmv,
    SUM(freight_value) AS freight
  FROM fact_orders GROUP BY 1
)
SELECT *, freight / NULLIF(gmv, 0) AS freight_to_gmv
FROM state_totals ORDER BY freight_to_gmv DESC;

CREATE OR REPLACE TABLE review_outcomes AS
SELECT is_late, COUNT(*) AS orders, AVG(review_score) AS mean_review,
  MEDIAN(review_score) AS median_review
FROM fact_orders WHERE order_status='delivered' AND review_score IS NOT NULL GROUP BY 1;

CREATE OR REPLACE TABLE customer_cohorts AS
WITH qualifying AS (
  SELECT customer_unique_id, purchase_ts, date_trunc('month', purchase_ts) AS purchase_month
  FROM fact_orders WHERE order_status NOT IN ('canceled', 'unavailable')
), firsts AS (
  SELECT customer_unique_id, MIN(purchase_month) AS cohort_month FROM qualifying GROUP BY 1
), cells AS (
  SELECT f.cohort_month, q.purchase_month,
    date_diff('month', f.cohort_month, q.purchase_month) AS months_since_first,
    COUNT(DISTINCT q.customer_unique_id) AS retained_customers
  FROM qualifying q JOIN firsts f USING(customer_unique_id)
  GROUP BY 1, 2, 3
), sizes AS (SELECT cohort_month, COUNT(*) AS cohort_customers FROM firsts GROUP BY 1)
SELECT c.*, s.cohort_customers,
  c.retained_customers * 1.0 / NULLIF(s.cohort_customers, 0) AS retention_rate
FROM cells c JOIN sizes s USING(cohort_month)
ORDER BY cohort_month, months_since_first;

CREATE OR REPLACE TABLE rfm_customer AS
WITH base AS (
  SELECT customer_unique_id,
    date_diff('day', MAX(purchase_ts), (SELECT MAX(purchase_ts) FROM fact_orders)) AS recency,
    COUNT(*) AS frequency, SUM(gmv) AS monetary
  FROM fact_orders WHERE order_status NOT IN ('canceled', 'unavailable')
  GROUP BY 1
), scored AS (
  SELECT *, NTILE(5) OVER (ORDER BY recency DESC, customer_unique_id) AS r_score,
    NTILE(5) OVER (ORDER BY frequency, customer_unique_id) AS f_score,
    NTILE(5) OVER (ORDER BY monetary, customer_unique_id) AS m_score
  FROM base
)
SELECT *, r_score + f_score + m_score AS combined_score,
  CASE
    WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
    WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal'
    WHEN r_score >= 4 AND f_score <= 2 THEN 'Potential Loyalists'
    WHEN r_score >= 4 THEN 'Recent'
    WHEN r_score <= 2 AND f_score <= 2 THEN 'At Risk'
    ELSE 'Needs Attention'
  END AS segment
FROM scored;

CREATE OR REPLACE TABLE rfm_segments AS
SELECT segment, COUNT(*) AS customers, SUM(monetary) AS monetary,
  AVG(recency) AS avg_recency, AVG(frequency) AS avg_frequency,
  COUNT(*) * 1.0 / SUM(COUNT(*)) OVER () AS customer_share
FROM rfm_customer GROUP BY 1 ORDER BY monetary DESC;

CREATE OR REPLACE TABLE category_pareto AS
SELECT category, gmv, orders, gmv_rank, cumulative_gmv_share,
  CASE WHEN cumulative_gmv_share <= 0.8 THEN TRUE ELSE FALSE END AS within_80pct
FROM category_kpis ORDER BY gmv DESC;
