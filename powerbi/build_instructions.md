# Power BI build instructions

1. Run the pipeline through `python -m src.build_dashboard_data`.
2. Open `powerbi/OlistMarketplace.pbip` in Power BI Desktop.
3. The validated project imports `data/published/fact_orders.csv` and `dim_date.csv`.
4. The model contains explicit order-grain measures and date relationships.
5. The report contains three pages: Executive Overview, Fulfillment & CX,
   and Customer & Growth.

The checked-in PBIP is the primary report artifact. Desktop reopened it with zero
Problems, rendered the three pages, and calculated the headline measures.
