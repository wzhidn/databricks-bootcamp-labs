-- Bronze layer: land raw files incrementally. Built in lab 01.
-- ${raw_path} comes from the pipeline configuration in resources/ingestion.pipeline.yml.

-- Reference data (small, re-read on every update)
CREATE OR REFRESH MATERIALIZED VIEW customers
COMMENT "Customer master data from the raw volume"
AS SELECT *
FROM read_files('${raw_path}/customers/', format => 'json');

CREATE OR REFRESH MATERIALIZED VIEW products
COMMENT "Product catalogue from the raw volume"
AS SELECT *
FROM read_files('${raw_path}/products/', format => 'json');

CREATE OR REFRESH STREAMING TABLE orders_bronze
COMMENT "Raw orders ingested incrementally with Auto Loader"
AS SELECT
  *,
  _metadata.file_path AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files(
  '${raw_path}/orders/',
  format => 'json',
  schemaEvolutionMode => 'addNewColumns'
);
