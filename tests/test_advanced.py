import os
from pathlib import Path

import duckdb

DB = Path(os.environ.get("OLIST_DB_PATH", "data/processed/olist.duckdb"))


def test_advanced_outputs_exist():
    con = duckdb.connect(str(DB), read_only=True)
    tables = {r[0] for r in con.sql("SHOW TABLES").fetchall()}
    con.close()
    assert {"customer_cohorts", "rfm_customer", "rfm_segments", "category_pareto"} <= tables


def test_cohort_month_zero_is_full_cohort():
    con = duckdb.connect(str(DB), read_only=True)
    bad = con.sql("SELECT COUNT(*) FROM customer_cohorts WHERE months_since_first=0 AND retention_rate != 1").fetchone()[0]
    con.close()
    assert bad == 0


def test_rfm_scores_are_quantile_bounded():
    con = duckdb.connect(str(DB), read_only=True)
    bad = con.sql("SELECT COUNT(*) FROM rfm_customer WHERE r_score NOT BETWEEN 1 AND 5 OR f_score NOT BETWEEN 1 AND 5 OR m_score NOT BETWEEN 1 AND 5").fetchone()[0]
    con.close()
    assert bad == 0


def test_seller_analysis_applies_volume_threshold():
    con = duckdb.connect(str(DB), read_only=True)
    bad = con.sql("SELECT COUNT(*) FROM seller_kpis WHERE orders < 20").fetchone()[0]
    con.close()
    assert bad == 0


def test_pareto_share_is_monotone():
    con = duckdb.connect(str(DB), read_only=True)
    bad = con.sql("SELECT COUNT(*) FROM (SELECT cumulative_gmv_share, LAG(cumulative_gmv_share) OVER (ORDER BY gmv DESC) previous FROM category_pareto) WHERE previous IS NOT NULL AND cumulative_gmv_share < previous").fetchone()[0]
    con.close()
    assert bad == 0


def test_cohort_output_has_required_grain_fields():
    con = duckdb.connect(str(DB), read_only=True)
    columns = {r[0] for r in con.sql("DESCRIBE customer_cohorts").fetchall()}
    con.close()
    assert {"cohort_month", "months_since_first", "retained_customers", "retention_rate"} <= columns


def test_freight_ratios_are_nonnegative():
    con = duckdb.connect(str(DB), read_only=True)
    bad = con.sql("SELECT COUNT(*) FROM freight_state WHERE freight_to_gmv < 0").fetchone()[0]
    con.close()
    assert bad == 0


def test_review_outcomes_have_both_delivery_groups():
    con = duckdb.connect(str(DB), read_only=True)
    groups = {r[0] for r in con.sql("SELECT is_late FROM review_outcomes").fetchall()}
    con.close()
    assert groups == {True, False}
