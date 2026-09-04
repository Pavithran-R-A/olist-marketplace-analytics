# Interview walkthrough

## 30-second answer

I built an Olist marketplace analytics project for leadership decisions around GMV, delivery,
freight, reviews, and repeat customers. I used Python for acquisition and validation, DuckDB
and SQL for a grain-safe model and KPIs, SciPy for the late-versus-on-time comparison, and
Plotly plus a validated Power BI report for communication.

## 90-second answer

The core design uses one row per order in `fact_orders`, with item merchandise and freight
pre-aggregated before customer and review joins. That prevents fanout. I found R$13.59M GMV,
8.11% late delivery, 16.57% freight-to-GMV, and a 3.04% repeat-customer rate. Late orders
averaged 2.57 reviews versus 4.29 on time. I describe that as association because the data
does not identify causation.

## Technical walkthrough

The raw CSVs are profiled first. DuckDB loads them locally. SQL creates the order and item
facts, cohort retention, quintile-based RFM segments, and business outputs. Python exports
reproducible tables and dashboard data. Tests cover KPI math, timestamp logic, late flags,
negative monetary detection, and RFM labeling. Power BI assets
define measures and relationships. The three report pages map to executive, fulfillment,
and customer-growth decisions. Plotly provides the browser demo; Power BI provides
BI-tool evidence.

## Likely questions

- **Why this dataset?** It has related marketplace facts and realistic grain risks.
- **How did you prevent double counting?** Aggregate items before joining to orders.
- **Why DuckDB?** It is local, fast, reproducible, and SQL-first.
- **What is GMV?** Sum of item prices; it is not recognized revenue.
- **How is late delivery defined?** Actual customer delivery after estimated date.
- **How is repeat defined?** More than one order by unique customer identity.
- **What would production change?** Add tested SLA history, carrier data, costs, and monitoring.
