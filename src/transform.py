from __future__ import annotations

from .common import connection, csv_files
from .config import DB_PATH


def transform() -> None:
    con = connection()
    for path in csv_files():
        table = path.stem.replace("_dataset", "").replace("olist_", "").replace("product_category_name_translation", "category_translation")
        con.execute(f"CREATE OR REPLACE TABLE raw_{table} AS SELECT * FROM read_csv_auto(?, header=true)", [str(path)])
    con.execute("""
    CREATE OR REPLACE TABLE fact_orders AS
    SELECT o.order_id, o.customer_id, c.customer_unique_id, c.customer_state,
      CAST(o.order_purchase_timestamp AS TIMESTAMP) AS purchase_ts,
      CAST(o.order_delivered_customer_date AS TIMESTAMP) AS delivered_ts,
      CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS estimated_ts,
      o.order_status, COALESCE(i.gmv, 0) AS gmv, COALESCE(i.freight_value, 0) AS freight_value,
      COALESCE(i.items, 0) AS items,
      CASE WHEN o.order_status='delivered' AND o.order_delivered_customer_date IS NOT NULL
        AND o.order_estimated_delivery_date IS NOT NULL
        AND CAST(o.order_delivered_customer_date AS TIMESTAMP) > CAST(o.order_estimated_delivery_date AS TIMESTAMP)
        THEN TRUE ELSE FALSE END AS is_late,
      CASE WHEN o.order_status='delivered' AND o.order_delivered_customer_date IS NOT NULL
        THEN date_diff('day', CAST(o.order_purchase_timestamp AS TIMESTAMP), CAST(o.order_delivered_customer_date AS TIMESTAMP)) END AS delivery_days,
      r.review_score
    FROM raw_orders o
    LEFT JOIN raw_customers c USING (customer_id)
    LEFT JOIN (SELECT order_id, SUM(price) AS gmv, SUM(freight_value) AS freight_value, COUNT(*) AS items
      FROM raw_order_items GROUP BY order_id) i USING (order_id)
    LEFT JOIN (SELECT order_id, AVG(review_score) AS review_score
      FROM raw_order_reviews GROUP BY order_id) r USING (order_id)
    """)
    con.execute("""
    CREATE OR REPLACE TABLE fact_order_items AS
    SELECT i.*, p.product_category_name, COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') AS category
    FROM raw_order_items i LEFT JOIN raw_products p USING(product_id)
    LEFT JOIN raw_category_translation t USING(product_category_name)
    """)
    con.execute("CREATE OR REPLACE TABLE fact_payments AS SELECT * FROM raw_order_payments")
    con.execute("CREATE OR REPLACE TABLE dim_customers AS SELECT * FROM raw_customers")
    con.execute("CREATE OR REPLACE TABLE dim_sellers AS SELECT * FROM raw_sellers")
    con.execute("CREATE OR REPLACE TABLE dim_products AS SELECT p.*, COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') AS category FROM raw_products p LEFT JOIN raw_category_translation t USING(product_category_name)")
    con.execute("CHECKPOINT")
    con.close()
    print(f"Created analytical model at {DB_PATH}")


if __name__ == "__main__":
    transform()
