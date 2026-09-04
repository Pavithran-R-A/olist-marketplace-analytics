# Power BI build instructions

1. Run the pipeline through `python -m src.build_dashboard_data`.
2. Load `data/processed/olist.duckdb` in Power BI Desktop.
3. Add the `fact_orders`, `fact_order_items`, and dimensions documented in `model.tmdl`.
4. Create the measures from `measures.dax`.
5. Add an explicit date table and three pages: Executive Overview, Fulfillment & CX,
   and Customer & Growth.

The supplied TMDL and DAX are source-control-friendly specifications. Power BI Desktop is
not installed here, so no PBIP opening or visual rendering claim is made.

