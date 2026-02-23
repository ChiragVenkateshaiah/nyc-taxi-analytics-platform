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


