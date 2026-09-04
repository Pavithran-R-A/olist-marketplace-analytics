# Executive Summary

The observed marketplace generated R$13.59M GMV across 99,441 orders. Delivery reliability
is the clearest customer-experience risk: late orders score materially lower, while freight
absorbs a meaningful share of merchandise value. Repeat purchasing is limited in the dataset
window, suggesting retention deserves a focused operating response.

# 5 Key Findings

1. GMV was R$13,591,643.70 across 99,441 orders, producing an average order value of
   R$136.68.
2. Late delivery was observed for 8.11% of delivered orders with comparable dates.
3. Late deliveries averaged 2.57 review points versus 4.29 for on-time deliveries, a
   difference of -1.73 points. The Mann-Whitney comparison returned p < 0.001; this is
   association, not causal proof.
4. Freight totaled R$2,251,909.54, equal to 16.57% of GMV.
5. Only 2,997 of 96,096 observed customers purchased more than once, a repeat-customer
   rate of 3.12% within this dataset window.

# 5 Recommended Actions

1. Finding -> late delivery is linked with a 1.73-point review gap -> prioritize carrier
   and seller exception queues for high-volume late-risk lanes.
2. Finding -> RJ has 12.95% late rate versus 5.72% in SP -> investigate regional carrier
   capacity, promised dates, and seller handoff performance in RJ.
3. Finding -> freight is 16.57% of GMV -> review packaging, seller shipping policies, and
   high-freight item categories using a freight-burden monitor.
4. Finding -> repeat rate is 3.12% -> test post-delivery reactivation journeys and measure
   second-order conversion by cohort.
5. Finding -> health_beauty leads categories at R$1.26M GMV -> protect service levels for
   leading categories while targeting cross-sell into adjacent repeatable categories.

# Methodology Notes

GMV sums item prices. Items and payments remain separate grains. Delivery flags require a
delivered status plus both actual and estimated dates. Review scores are averaged per order.
Customer identity uses `customer_unique_id`. Full computed outputs are under `reports/`.

# Limitations

The data is historical and anonymized. It does not contain marketplace commission revenue,
cost-to-serve, carrier identity, promised SLA versions, or customer marketing exposure.
Repeat rate is limited by the observation window. Geolocation duplicates were excluded from
the core model. Dashboard values are descriptive, not causal forecasts.

