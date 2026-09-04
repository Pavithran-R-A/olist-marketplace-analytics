from pathlib import Path

import duckdb
import pytest

DB = Path("data/processed/olist.duckdb")


pytestmark = pytest.mark.skipif(not DB.exists(), reason="full-data model not acquired")


def test_order_model_reconciles_source_orders_and_gmv():
    con = duckdb.connect(str(DB), read_only=True)
    order_count = con.sql("SELECT COUNT(*) FROM fact_orders").fetchone()[0]
    source_count = con.sql("SELECT COUNT(DISTINCT order_id) FROM raw_orders").fetchone()[0]
    model_gmv = con.sql("SELECT SUM(gmv) FROM fact_orders").fetchone()[0]
    source_gmv = con.sql("SELECT SUM(price) FROM raw_order_items").fetchone()[0]
    con.close()
    assert order_count == source_count == 99441
    assert model_gmv == pytest.approx(source_gmv)


def test_fact_orders_has_no_duplicate_order_keys():
    con = duckdb.connect(str(DB), read_only=True)
    duplicates = con.sql("SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM fact_orders").fetchone()[0]
    con.close()
    assert duplicates == 0

