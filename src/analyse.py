from __future__ import annotations

import json
import math

import numpy as np
from scipy.stats import mannwhitneyu

from .common import connection
from .config import REPORTS
from .run_sql import run_sql


def _mean_stats(values: np.ndarray) -> dict[str, float]:
    mean = float(values.mean())
    se = float(values.std(ddof=1) / math.sqrt(len(values))) if len(values) > 1 else 0.0
    return {"n": len(values), "mean": mean, "median": float(np.median(values)),
            "ci95_low": mean - 1.96 * se, "ci95_high": mean + 1.96 * se}


def analyse() -> dict[str, object]:
    run_sql()
    con = connection()
    kpi = con.sql("""
      SELECT SUM(gmv) gmv, COUNT(*) orders, COUNT(DISTINCT customer_unique_id) customers,
        AVG(gmv) aov, SUM((order_status='delivered')::INT) delivered_orders,
        SUM((order_status='canceled')::INT) cancelled_orders,
        AVG(CASE WHEN order_status='delivered' THEN is_late::INT END) late_delivery_rate,
        AVG(review_score) avg_review, AVG(items) items_per_order, SUM(freight_value) freight
      FROM fact_orders
    """).fetchone()
    names = ["gmv", "orders", "customers", "aov", "delivered_orders", "cancelled_orders",
             "late_delivery_rate", "avg_review", "items_per_order", "freight"]
    result = dict(zip(names, kpi))
    late = con.sql("SELECT review_score FROM fact_orders WHERE order_status='delivered' AND is_late AND review_score IS NOT NULL").fetchnumpy()["review_score"]
    ontime = con.sql("SELECT review_score FROM fact_orders WHERE order_status='delivered' AND NOT is_late AND review_score IS NOT NULL").fetchnumpy()["review_score"]
    late_stats, ontime_stats = _mean_stats(late), _mean_stats(ontime)
    diff = float(late.mean() - ontime.mean())
    pooled = math.sqrt(((len(late)-1)*late.var(ddof=1) + (len(ontime)-1)*ontime.var(ddof=1)) / (len(late)+len(ontime)-2)) if len(late) > 1 and len(ontime) > 1 else float("nan")
    variance = (late.var(ddof=1) / len(late) if len(late) > 1 else 0.0) + (ontime.var(ddof=1) / len(ontime) if len(ontime) > 1 else 0.0)
    result.update({"late_review": late_stats, "ontime_review": ontime_stats,
                   "review_difference": diff,
                   "review_difference_ci95_low": diff - 1.96 * math.sqrt(variance),
                   "review_difference_ci95_high": diff + 1.96 * math.sqrt(variance),
                   "mann_whitney_p": float(mannwhitneyu(late, ontime, alternative='two-sided').pvalue),
                   "cohens_d": diff / pooled})
    repeat = con.sql("SELECT COUNT(*) FILTER (WHERE frequency > 1), COUNT(*) FROM rfm_customer").fetchone()
    result.update({"repeat_customers": int(repeat[0]), "repeat_customer_rate": float(repeat[0] / repeat[1]), "freight_to_gmv": float(result["freight"] / result["gmv"])})
    export_names = ["monthly_kpis", "status_kpis", "category_kpis", "state_kpis", "seller_kpis",
                    "fulfillment_category", "freight_state", "review_outcomes", "customer_cohorts",
                    "rfm_segments", "category_pareto"]
    REPORTS.mkdir(parents=True, exist_ok=True)
    for name in export_names:
        con.table(name).df().to_csv(REPORTS / f"{name}.csv", index=False)
    (REPORTS / "kpis.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    con.close()
    print(json.dumps(result, indent=2, default=str))
    return result


if __name__ == "__main__":
    analyse()
