-- Silver layer: typed, cleaned and quality-checked orders. Built in lab 01.
-- The rules mirror src/bootcamp_lib/quality.py, which is unit-tested in CI (lab 06).

CREATE OR REFRESH STREAMING TABLE orders_silver
-- SOLUTION-BEGIN lab-01: Add a constraint list in parentheses with three expectations: drop rows without customer_id, drop rows with amount <= 0, and only warn (keep) when region is not one of EMEA, NA, LATAM, APAC.
(
  CONSTRAINT has_customer    EXPECT (customer_id IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT positive_amount EXPECT (amount > 0)              ON VIOLATION DROP ROW,
  CONSTRAINT known_region    EXPECT (region IN ('EMEA', 'NA', 'LATAM', 'APAC'))
)
-- SOLUTION-END
COMMENT "Cleaned orders with data quality expectations"
AS SELECT
  CAST(order_id AS BIGINT)        AS order_id,
  CAST(customer_id AS BIGINT)     AS customer_id,
  CAST(product_id AS BIGINT)      AS product_id,
  CAST(quantity AS INT)           AS quantity,
  CAST(amount AS DECIMAL(12, 2))  AS amount,
  channel,
  CAST(order_ts AS TIMESTAMP)     AS order_ts,
  to_date(order_ts)               AS order_date,
  upper(trim(region))             AS region,
  -- SOLUTION-BEGIN lab-01: After the schema-drift batch lands (with_coupon=true), add coupon_code to the select list.
  -- coupon_code,
  -- SOLUTION-END
  source_file
FROM STREAM(orders_bronze);
