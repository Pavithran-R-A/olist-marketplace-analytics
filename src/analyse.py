from __future__ import annotations

import json

from scipy.stats import mannwhitneyu

from .common import connection
from .config import REPORTS


def analyse() -> dict[str, object]:
    con = connection()
    kpi = con.sql("""
      SELECT SUM(gmv) gmv, COUNT(*) orders, COUNT(DISTINCT customer_unique_id) customers,
        AVG(gmv) aov, SUM(CASE WHEN order_status='delivered' THEN 1 ELSE 0 END) delivered_orders,
        SUM(CASE WHEN order_status='canceled' THEN 1 ELSE 0 END) cancelled_orders,
        AVG(CASE WHEN order_status='delivered' THEN is_late::INT END) late_delivery_rate,
        AVG(review_score) avg_review, AVG(items) items_per_order, SUM(freight_value) freight
      FROM fact_orders
    """).df().iloc[0].to_dict()
    monthly = con.sql("SELECT date_trunc('month', purchase_ts) AS month, SUM(gmv) gmv, COUNT(*) orders FROM fact_orders GROUP BY 1 ORDER BY 1").df()
    category = con.sql("SELECT category, SUM(price) gmv, COUNT(DISTINCT order_id) orders FROM fact_order_items GROUP BY 1 ORDER BY gmv DESC LIMIT 15").df()
    states = con.sql("SELECT customer_state state, SUM(gmv) gmv, COUNT(*) orders, AVG(is_late::INT) late_rate, AVG(review_score) avg_review FROM fact_orders GROUP BY 1 ORDER BY gmv DESC").df()
    seller = con.sql("SELECT seller_id, SUM(price) gmv, COUNT(DISTINCT order_id) orders, AVG(CASE WHEN fo.order_status='delivered' THEN fo.is_late::INT END) late_rate FROM fact_order_items oi JOIN fact_orders fo USING(order_id) GROUP BY seller_id HAVING COUNT(DISTINCT order_id)>=20 ORDER BY late_rate DESC LIMIT 20").df()
    review = con.sql("SELECT is_late, AVG(review_score) avg_review, COUNT(*) orders FROM fact_orders WHERE review_score IS NOT NULL AND order_status='delivered' GROUP BY 1").df()
    customers = con.sql("SELECT customer_unique_id, COUNT(*) frequency, SUM(gmv) monetary, date_diff('day', MAX(purchase_ts), (SELECT MAX(purchase_ts) FROM fact_orders)) recency FROM fact_orders GROUP BY 1").df()
    late = review.loc[review.is_late == True, "avg_review"]
    ontime = review.loc[review.is_late == False, "avg_review"]
    customer_groups = [customers.loc[customers.frequency > 1, "customer_unique_id"].nunique(), customers.loc[customers.frequency == 1, "customer_unique_id"].nunique()]
    if len(late) and len(ontime):
        late_rows = con.sql("SELECT review_score FROM fact_orders WHERE order_status='delivered' AND is_late AND review_score IS NOT NULL").df().review_score
        ontime_rows = con.sql("SELECT review_score FROM fact_orders WHERE order_status='delivered' AND NOT is_late AND review_score IS NOT NULL").df().review_score
        stat = mannwhitneyu(late_rows, ontime_rows, alternative="two-sided")
        kpi.update({"late_avg_review": float(late.iloc[0]), "ontime_avg_review": float(ontime.iloc[0]), "review_difference": float(late.iloc[0] - ontime.iloc[0]), "mann_whitney_p": float(stat.pvalue)})
    kpi.update({"repeat_customers": customer_groups[0], "repeat_customer_rate": customer_groups[0] / sum(customer_groups), "freight_to_gmv": float(kpi["freight"] / kpi["gmv"])})
    REPORTS.mkdir(parents=True, exist_ok=True)
    for name, frame in [("monthly", monthly), ("category", category), ("states", states), ("seller", seller), ("review", review), ("customers", customers)]:
        frame.to_csv(REPORTS / f"{name}.csv", index=False)
    (REPORTS / "kpis.json").write_text(json.dumps(kpi, indent=2, default=str), encoding="utf-8")
    con.close()
    print(json.dumps(kpi, indent=2, default=str))
    return kpi


if __name__ == "__main__":
    analyse()

