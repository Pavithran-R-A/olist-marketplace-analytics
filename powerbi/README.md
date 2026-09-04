# Power BI source package

This folder contains a Power BI Desktop-validated PBIP project. Desktop generated and
reopened the PBIR report and TMDL semantic model. The model imports the reproducible
order-grain `fact_orders` table and `dim_date`, with explicit DAX measures for GMV,
orders, customers, AOV, fulfillment, freight, reviews, and repeat customers.
Microsoft's official [TMDL overview](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview)
defines the object syntax used here.
