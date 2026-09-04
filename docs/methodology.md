# Methodology

The model begins with order items, then pre-aggregates item merchandise and freight to
order grain before joining customer and review data. This prevents payment or item fanout.

Late delivery compares the customer delivery timestamp with the estimated delivery date,
only for delivered orders with both dates. Review analysis reports the difference in means,
the observed distributions, and a two-sided Mann-Whitney U test. This is association, not
causation. Cohorts use the month of each customer's first observed purchase. RFM recency
uses days since the latest purchase in the dataset window.

