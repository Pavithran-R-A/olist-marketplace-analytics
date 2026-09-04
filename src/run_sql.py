from __future__ import annotations

from .common import connection
from .config import ROOT


def run_sql() -> list[str]:
    con = connection()
    script = (ROOT / "sql" / "07_advanced_analytics.sql").read_text(encoding="utf-8")
    con.execute(script)
    names = ["monthly_kpis", "status_kpis", "category_kpis", "state_kpis", "seller_kpis",
             "fulfillment_category", "freight_state", "review_outcomes", "customer_cohorts",
             "rfm_customer", "rfm_segments", "category_pareto"]
    con.close()
    return names


if __name__ == "__main__":
    print(run_sql())

