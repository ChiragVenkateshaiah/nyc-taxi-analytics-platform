# 🧱 Data Model & Schemas
## NYC Taxi Analytics Platform (Databricks Lakehouse)

---

### 1. Purpose of This Document
This document defines the logical and physical data model for the NYC Taxi Analytics Platform, following the Databricks Lakehouse + Medallion Architecture.

It specifies:
- Table schemas per layer
- Data granularity (grain)
- Partitioning strategy
- Transformation responsibilities

This ensures scalability, performance, and consistency across the platform

---

### 2. Medallion Architecture Overview
| Layer  | Purpose          | Characteristics         |
| ------ | ---------------- | ----------------------- |
| Bronze | Raw ingestion    | Immutable, append-only  |
| Silver | Clean & enriched | Validated, standardized |
| Gold   | Business metrics | Aggregated, BI-ready    |

---

### 3. Bronze Layer - Raw Data Model
#### 📂 Table: `bronze_nyc_taxi_trips`

Purpose
- Store raw NYC Taxi trip data as-is
- Enable reprocessing and audit
- No business logic applied

Grain
> One row per taxi trip (raw event)

Schema

| Column Name         | Data Type | Description            |
| ------------------- | --------- | ---------------------- |
| vendor_id           | STRING    | Taxi vendor identifier |
| pickup_datetime     | TIMESTAMP | Pickup timestamp       |
| dropoff_datetime    | TIMESTAMP | Drop-off timestamp     |
| passenger_count     | INT       | Number of passengers   |
| trip_distance       | DOUBLE    | Distance in miles      |
| pickup_location_id  | INT       | Pickup zone ID         |
| dropoff_location_id | INT       | Drop-off zone ID       |
| fare_amount         | DOUBLE    | Fare charged           |
| tip_amount          | DOUBLE    | Tip amount             |
| tolls_amount        | DOUBLE    | Toll charges           |
| payment_type        | STRING    | Payment method         |
| total_amount        | DOUBLE    | Total charged          |
| ingestion_date      | DATE      | Load date              |

Storage
- Format: Delta
- Partitioned by: `ingestion_date`

---

### 4. Silver Layer - Cleaned & Enriched Model
#### 📂 Table: `silver_nyc_taxi_trips`

Purpose
- Clean invalid records
- Normalize data types
- Add derived and enrichment columns

Grain

> One row per valid taxi trip

Transformation Applied
- Remove records with invalid timestamps
- Filter negative fares/distances
- Standardize payment types
- Join zone lookup table

Schema

| Column Name           | Data Type | Description        |
| --------------------- | --------- | ------------------ |
| trip_id               | STRING    | Surrogate key      |
| pickup_datetime       | TIMESTAMP | Pickup timestamp   |
| dropoff_datetime      | TIMESTAMP | Drop-off timestamp |
| trip_date             | DATE      | Pickup date        |
| trip_hour             | INT       | Pickup hour        |
| passenger_count       | INT       | Passengers         |
| trip_distance         | DOUBLE    | Miles traveled     |
| trip_duration_minutes | DOUBLE    | Derived duration   |
| pickup_zone           | STRING    | Zone name          |
| dropoff_zone          | STRING    | Zone name          |
| fare_amount           | DOUBLE    | Fare               |
| tip_amount            | DOUBLE    | Tip                |
| tolls_amount          | DOUBLE    | Tolls              |
| total_amount          | DOUBLE    | Total              |
| payment_type          | STRING    | Normalized payment |
| is_valid_trip         | BOOLEAN   | Data quality flag  |

Storage:
- Format: Delta
- Partitioned by: `trip_date`

---

### 5. Gold Layer - Analytics Data Model
Gold tables are read-optimized, aggregated, and metric-driven

#### Table: `gold_revenue_metrics`

Grain

> One row per trip_date + pickup_zone

| Column Name   | Data Type | Description   |
| ------------- | --------- | ------------- |
| trip_date     | DATE      | Trip date     |
| pickup_zone   | STRING    | Pickup zone   |
| total_revenue | DOUBLE    | Total revenue |
| fare_revenue  | DOUBLE    | Fare revenue  |
| tip_revenue   | DOUBLE    | Tip revenue   |
| total_trips   | BIGINT    | Trip count    |
| avg_fare      | DOUBLE    | Avg fare      |

Partition
- `trip_date`

---

#### Table: `gold_trip_metrics`

Grain

> One row per trip_date + trip_hour + pickup_zone

| Column Name           | Data Type | Description  |
| --------------------- | --------- | ------------ |
| trip_date             | DATE      | Trip date    |
| trip_hour             | INT       | Hour of day  |
| pickup_zone           | STRING    | Pickup zone  |
| total_trips           | BIGINT    | Trips        |
| avg_trip_distance     | DOUBLE    | Avg distance |
| avg_trip_duration_min | DOUBLE    | Avg duration |

Partition
- `trip_date`

#### Table: `gold_customer_metrics`

Grain

> One row per trip_date + pickup_zone

| Column Name        | Data Type | Description |
| ------------------ | --------- | ----------- |
| trip_date          | DATE      | Trip date   |
| pickup_zone        | STRING    | Pickup zone |
| avg_tip_percentage | DOUBLE    | Avg tip %   |
| cash_payments      | BIGINT    | Cash trips  |
| card_payments      | BIGINT    | Card trips  |
| total_trips        | BIGINT    | Trips       |

Partition
- `trip_date`

#### Table: `gold_efficiency_metrics`

Grain
> One row per trip_date + pickup_zone

| Column Name          | Data Type | Description            |
| -------------------- | --------- | ---------------------- |
| trip_date            | DATE      | Trip date              |
| pickup_zone          | STRING    | Pickup zone            |
| revenue_per_mile     | DOUBLE    | Revenue efficiency     |
| revenue_per_minute   | DOUBLE    | Time efficiency        |
| short_low_fare_trips | BIGINT    | Inefficiency indicator |

Partition
- `trip_date`

---

### 6. Partitioning Strategy
| Layer  | Partition Column | Reason                |
| ------ | ---------------- | --------------------- |
| Bronze | ingestion_date   | Incremental loads     |
| Silver | trip_date        | Time-based pruning    |
| Gold   | trip_date        | BI query optimization |

### 7. Data Modeling Best Practices Applied
- Star-schema-friendly Gold layer
- Clear grain definition per table
- No joins required at BI layer
- Delta Lake ACID compliance
- Schema evolution supported

---

### 8. End-to-End Lineage
```pgsql
Bronze (raw trips)
      ↓
Silver (clean + enriched trips)
      ↓
Gold (business metrics tables)
      ↓
Databricks SQL / BI Dashboards
```