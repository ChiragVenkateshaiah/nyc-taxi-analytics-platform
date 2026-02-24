# Silver Layer Implementation - Production Guide

---

## Overview

This Silver layer implementation transforms raw Bronze data into a production-ready dimensional model with:

- ✅ Schema standardization (Green & Yellow taxi datasets)
- ✅ Unified fact table (`fact_taxi_trips`)
- ✅ SCD Type 2 dimension table (`dim_taxi_zone`)
- ✅ Comprehensive data quality checks
- ✅ Error handling and validation
- ✅ Audit trail tracking
- ✅ Idempotent processing

---

## Architecture

```python
Bronze Layer (Raw Delta Tables)
    ├── green/
    └── yellow/
           ↓
    [Schema Standardization]
           ↓
Silver Layer (Dimensional Model)
    ├── green_standardized/      [Intermediate]
    ├── yellow_standardized/     [Intermediate]
    ├── fact_taxi_trips/         [Fact Table]
    └── dim_taxi_zone/           [SCD Type 2 Dimension]
           ↓
Gold Layer (Business Metrics)
```

---

## Data Model

### Fact Table: `fact_taxi_trips`

| Column Name         | Data Type | Description                            |
| ------------------- | --------- | ----------------------                 |
| trip_id             | BIGINT    | Surrogate Key (auto-generated)         |
| taxi_type           | STRING    | "green" or "yellow"                    |
| vendor_id           | INT       | Vendor identifier                      |
| pickup_ts           | TIMESTAMP | Pickup timestamp                       |
| dropoff_ts          | TIMESTAMP | Dropoff timestamp                      |
| passenger_count     | INT       | Number of passengers (1-9)             |
| trip_distance       | DOUBLE    | Trip distance in miles                 |
| fare_amount         | DOUBLE    | Base fare amount                       |
| total_amount        | DOUBLE    | Total amount paid                      |
| pickup_location_id  | INT       | Pickup LocationID (FK to dimension)    |
| dropoff_location_id | INT       | Dropoff LocationID (FK to dimension)   |
| year                | INT       | Partition key                          |
| month               | INT       | Partition Key                          |
| bronze_ingestion_ts | TIMESTAMP | Bronze layer ingestion timestamp       |
| silver_transformation_ts | TIMESTAMP    | Silver layer transformation timestamp 
| batch_id           | STRING | Batch identifier for auditability     |


**Partitioning:** By `year` and `month` for optimal query performance

---

### Dimension Table: `dim_taxi_zone` (SCD Type 2)

| Column Name         | Data Type | Description                            |
| ------------------- | --------- | ----------------------                 |
| zone_sk             | BIGINT    | Surrogate Key (auto-generated)         |
| location_id         | INT       | Natural key(NYCLocationID)             |
| borough             | STRING    | Borough name (Manhattan,Brooklyn, etc)               |
| zone           | STRING | Zone name                       |
| service_zone          | STRING | Service classification                  |
| effective_start_date       | DATE    | Record validity start date                 |
| effective_end_date         | DATE    | Record validity end date (9999-12-31 for current)                       |
| is_current        | BOOLEAN    | True if this is the current version                      |


#### SCD Type 2 Behavior:
- When a zone attribute changes (e.g., zone name updated):
       
       1. Existing active record: `effective_end_date` updated, `is_current` set to False

       2. New record inserted: New `zone_sk`, updated attributes, `is_current` = True


---

## Data Quality Framework

#### Validation Rules Applied

The `DataQualityChecker` class enforces the following rules:

Fact Table Quality Checks:

1. Null Timestamp Removal: Records with null `pickup_ts` or `dropoff_ts` are dropped
2. Invalid Distance: Records with `trip_distance <= 0` are dropped
3. Negative Fare: Records with `fare_amount < 0` are dropped
4. Negative Total: Records with `total_amount < 0` are dropped
5. Passenger Count Normalization: Values outside 1-9 are set to 1
6. Time Logic Validation: Records where `dropoff_ts <= pickup_ts` are dropped


#### Dimension Table Quality Checks:

1. Null Natural Key: Records with null `LocationID` are dropped


#### Quality Metrics Tracked

Each dataset reports:

- Initial row count
- Rows dropped per validation rule
- Final row count
- Retention rate (%)

---

### Schema Standardization

#### Green Taxi -> Unified Schema

| Bronze Column (Green) | Silver Column          |
| -------------------   | ---------              |
| lpep_pickup_datetime  | pickup_ts              |
| lpep_dropoff_datetime | dropoff_ts             |
| VendorID              | vendor_id              |
| PULocationID          | pickup_location_id     |
| DOLocationID          | dropoff_location_id    |


#### Yellow Taxi -> Unified Schema

| Bronze Column (Yellow)| Silver Column          |
| -------------------   | ---------              |
| tpep_pickup_datetime  | pickup_ts              |
| tpep_dropoff_datetime | dropoff_ts             |
| VendorID              | vendor_id              |
| PULocationID          | pickup_location_id     |
| DOLocationID          | dropoff_location_id    |


**Key Difference:** Green uses `lpep_*` prefixes, Yellow uses `tpep_*` prefixes. Both are standardized to the same unified schema.

---

## Prerequisites

#### 1. Bronze Layer Data

Ensure Bronze layer ingestion has completed successfully:

```python
data/bronze/nyc_taxi/
    ├── green/       [Delta Lake table]
    └── yellow/      [Delta Lake table]
```

#### 2. Taxi Zone Lookup Data

Download the taxi zone lookup CSV:

```bash
# Create lookup directory
mkdir -p data/lookup

# Download from NYC TLC
curl -o data/lookup/taxi_zone_lookup.csv \
  https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Or manually download from : https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page


Expected file location:
```bash
C:\Users\chira\Desktop\data_engineering\PySpark\nyc-taxi-analytics-platform\data\lookup\taxi_zone_lookup.csv
```

---

## How to Run

#### Option 1: Run as Notebook

1. Copy the script content to a Jupyter Notebook
2. Execute cells sequentially
3. Monitor output for quality metrics and errors


#### Option 2: Run as Python Script

```bash
cd C:\Users\chira\Desktop\data_engineering\PySpark\nyc-taxi-analytics-platform

python silver_layer_ingestion.py
```


#### Expected Output

```bash
############################################################
NYC TAXI ANALYTICS - SILVER LAYER INGESTION
Batch ID: batch_20250222_143052
############################################################

============================================================
STEP 1: Reading Bronze Layer Data
============================================================
  ✔ Loaded GREEN: 45,234 records
  ✔ Loaded YELLOW: 123,456 records

============================================================
STEP 2: Schema Standardization
============================================================
✔ Standardized 45,234 GREEN taxi records
✔ Standardized 123,456 YELLOW taxi records

============================================================
STEP 3: Fact Table Creation
============================================================

────────────────────────────────────────────────────────────
Data Quality Validation: GREEN
────────────────────────────────────────────────────────────
  Initial row count: 45,234
  ✔ Dropped 12 rows with null timestamps
  ✔ Dropped 3 rows with invalid trip_distance
  ✔ Dropped 0 rows with negative fare_amount
  ...

  Total dropped: 18 (0.04%)
  Retention rate: 99.96%

[Similar output for YELLOW dataset]

────────────────────────────────────────────────────────────
Fact Table Statistics
────────────────────────────────────────────────────────────
  Total trips:        168,672
  Total passengers:   287,543
  Total distance:     453,219.45 miles
  Total revenue:      $2,345,678.90

✔ Fact table written successfully

============================================================
STEP 4: Dimension Table (SCD Type 2)
============================================================
✔ Loaded 265 taxi zone records
✔ Created 265 dimension records (all current)

✅ SILVER LAYER INGESTION COMPLETED SUCCESSFULLY
```

---

## Error Handling

#### Built-in Error Recovery

1. Missing Bronze Data: Script validates Bronze tables exist before processing
2. Missing Lookup Data: Dimension creation is skipped gracefully (fact table still created)
3. Quality Check Failures: Detailed metrics show which records were dropped and why
4. Write Failures: Full stack traces provided for debugging


#### What to Do if Ingestion Fails

1. Check Bronze Layer:

       - Ensure Bronze ingestion completed successfully
       - Verify Delta tables exist: `data/bronze/nyc_taxi/green/` and `.../yellow/`

2. Check Lookup File:

       - Verify file exists: `data/lookup/taxi_zone_lookup.csv`
       - Ensure file is not corrupted (should have ~265rows)

3. Review Error Messages:

       - Look for specific validation failures
       - Check stack traces for root cause

4. Rerun safely:

       - The script is idempotent (safe to rerun)
       - Uses `overwrite` mode for Silver tables
       - No data duplication risk


---

## Incremental Processing (Future Enhancement)

Currently, the Silver layer performs full refresh on each run. For production environments, consider:

1. Partition-level Processing:

       - Track last processed partition in Bronze
       - Only process new/updated partitions
       - Use `append` mode with dynamic partition overwrite.

2. Change Data Capture (CDC):

       - Read Bronze Delta table change log
       - Process only new inserts since last run

3. State Tracking:

       - Maintain `_processing_state` Delta table
       - Record last successful batch timestamp
       - Resume from last checkpoint on failure


---


## Querying Silver Data

### Query Fact Table

```python
df_fact = spark.read.format("delta").load("data/silver/nyc_taxi/fact_taxi_trips")

# Revenue by taxi_type
df_fact.groupBy("taxi_type") \
       .agg(
              count("*").alias("total_trips"),
              sum("total_amount").alias("total_revenue")
       ) \
       .show()
```
### Query Dimension Table

```python
df_dim = spark.read.format("delta").load("data/silver/nyc_taxi/dim_taxi_zone")

# Show current zones by borough
df_dim.filter(col("is_current") ==  True) \
       .groupBy("borough") \
       .count() \
       .show()

```

### Join Fact + Dimension

```python
df_trips_with_zones = df_fact.alias("f") \
       .join(
              df_dim.filter(col("is_current") == True).alias("d"),
              col("f.pickup_location_id") == col("d.location_id"),
              "left"
       ) \
       .select(
              "f.trip_id",
              "f.taxi_type",
              "f.total_amount",
              "d.borough",
              "d.zone"
       )

# Revenue by borough
df_trips_with_zones.groupBy("borough") \
       .agg(sum("total_amount").alias("revenue")) \
       .orderBy(col("revenue").desc()) \
       .show()

```

---

### Performance Optimization

#### Current Optimizations

1. Partitioning: Fact table partitioned by `year` and `month`
2. Coalesce on Passenger Count: Null values defaulted to 1 (avoids downstream issues)
3. Type Casting: Explicit type casting during standardization (prevents schema drift)
4. Delta Lake: ACID transactions, time travel, and schema enforcement

#### Future Optimizations

1. Z-Ordering:

```python
spark.sql("OPTIMIZE fact_taxi_trips ZORDER BY (pickup_location_id)")
```

2. Compaction:

```python
spark.sql("OPTIMIZE fact_taxi_trips")
spark.sql("VACUUM fact_taxi_trips RETAIN 168 HOURS")
```

3. Bloom Filters:

```python
spark.sql("""
       CREATE BLOOMFILTER INDEX ON fact_taxi_trips
       FOR COLUMNS (pickup_location_id, dropoff_location_id)
""")
```

---

## Troubleshooting

Issue: "Table or view not found: delta"

Solution: Ensure Delta Lake is properly configured in Spark session

Issue: "Path does not exist: data/bronze/nyc_taxi/green"

Solution: Run Bronze layer ingestion first

Issue: Low retention rate (<90%)

Solution: Investigate Bronze data quality issues. Run Bronze layer validation queries

Issue: Dimension table shows 0 records

Solution: Verify taxi zone lookup CSV is downloaded and accessible

---

## Next Steps

After successful Silver ingestion:

1. ✅ Verify data quality metrics
2. ✅ Run sample queries to validate joins
3. ✅ Document discovered data quality issues
4. ✅ Build Gold layer business metrics
5. ✅ Implement incremental processing (if needed)

---

### Author: Chirag Venkateshaiah
**Data Engineer**