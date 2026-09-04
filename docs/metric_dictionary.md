# Metric dictionary

| Metric | Definition |
|---|---|
| GMV | Sum of `price` from order items, one item row counted once. Merchandise value, not marketplace revenue. |
| Orders | Distinct `order_id` at order grain. |
| Delivered orders | Orders with status `delivered`. |
| Cancelled orders | Orders with status `canceled`. |
| Cancellation rate | Cancelled orders divided by all orders. |
| AOV | GMV divided by distinct orders. |
| Items per order | Item rows divided by distinct orders. |
| Freight value | Sum of order-item `freight_value`. |
| Freight / GMV | Freight value divided by GMV. |
| Average delivery days | Calendar days from purchase to customer delivery, delivered orders only. |
| Late orders | Delivered orders where delivery timestamp exceeds estimated delivery date. |
| Late delivery rate | Late orders divided by delivered orders with comparable dates. |
| Average review score | Mean order review score, pre-aggregated to one review value per order. |
| 1-star rate | One-star reviews divided by reviewed orders. |
| Repeat customer rate | Customers with more than one observed order divided by observed customers. |
| Customer lifetime merchandise value | Sum of observed GMV per unique customer in dataset window. |

Payments are not used as GMV because payment installments and item totals have different
grains. No commission or recognized revenue field exists.

