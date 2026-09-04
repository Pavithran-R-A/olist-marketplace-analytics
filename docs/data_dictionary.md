# Data dictionary

`fact_orders` has one row per order. It contains customer state, status, GMV, freight,
item count, delivery days, late flag, and average review score.

`fact_order_items` has one row per order-item-seller combination. It retains price,
freight, product, seller, and translated category. `fact_payments` has one row per payment
sequence. `dim_customers`, `dim_products`, and `dim_sellers` retain source dimensions.

The order key is `order_id`; customer identity for repeat analysis is `customer_unique_id`.
The source geolocation table is intentionally not modeled because its repeated zip rows can
create cardinality errors without a documented aggregation policy.

