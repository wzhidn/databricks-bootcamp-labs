-- Gold layer: business-ready aggregates. Built in lab 01.

CREATE OR REFRESH MATERIALIZED VIEW revenue_by_region_daily
COMMENT "Daily revenue and order count per region"
AS SELECT
  order_date,
  region,
  count(*)    AS orders,
  sum(amount) AS revenue
FROM orders_silver
GROUP BY ALL;

CREATE OR REFRESH MATERIALIZED VIEW orders_enriched
COMMENT "Orders joined with customer segment and product category"
AS SELECT
  o.*,
  c.segment,
  p.category
FROM orders_silver o
LEFT JOIN customers c USING (customer_id)
LEFT JOIN products p USING (product_id);
