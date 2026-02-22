# Silver Layer Desing - Production-Grade (Unified Green & Yellow)

## NYC Taxi Analytics Platform

---

### 1. Objective

The Silver layer transitions the platform from dataset-level transformation to a **production-grade** dimensional modeling layer.

Its purpose is to:

- Standardize heterogeneous taxi datasets (Green & Yellow)
- Merge them into a unified analytical fact model
- Integrate external lookup datasets
- Implement Slowly Changing Dimensions (SCD Type 2)
- Provide historically accurate, analytics-ready data for Gold

> Core Principle: Silver produces trusted, business-aligned models - not just cleaned datasets.

---

### 2. Target Architecture

```bash
Landing (Raw Files)
        ↓
Bronze (Dataset-specific Delta Tables)
        ↓
Silver (Data Modeling Layer)
    ├── fact_taxi_trips
    ├── dim_taxi_zone (SCD Type 2)
    └── dim_date (future enhancement)
        ↓
Gold (Business Metrics & Aggregations)
```

The Silver layer represents the **data warehouse modeling boundary** of the platform

---

### 3. Silver Layer Data Model

#### 3.1 Fact Table: fact_taxi_trips
This table unifies both Green and Yellow taxi datasets into a single analytical structure.

#### Source Tables
- silver.green_standardized
- silver.yellow_standardized

Each dataset is standardized before union to ensure schema compatibility.

#### 3.2 Standardized Schema

| Column              | Description                      |
| ------------------- | -------------------------------- |
| trip_id             | Surrogate key (generated)        |
| taxi_type           | green / yellow                   |
| vendor_id           | Vendor identifier                |
| pickup_ts           | Pickup timestamp                 |
| dropoff_ts          | Dropoff timestamp                |
| passenger_count     | Number of passengers             |
| trip_distance       | Distance in miles                |
| fare_amount         | Base fare                        |
| total_amount        | Total amount paid                |
| pickup_location_id  | Pickup LocationID (natural key)  |
| dropoff_location_id | Dropoff LocationID (natural key) |
| year                | Partition column                 |
| month               | Partition column                 |

---

#### 3.3 Design Principles

- Schema harmonization happens in Silver (not Bronze)
- taxi_type preserves dataset lineage
- Partitioning strategy: `year`, `month`
- No aggregations performed at this stage
- Designed for incremental ingestion

---

### 4. Lookup Table Integration

#### 4.1 Taxi Zone Lookup Dataset

The NYC Taxi & Limousine Commission publishes a taxi zone lookup file containing geographic metadata.

#### Lookup Schema

| Column       | Description            |
| ------------ | ---------------------- |
| LocationID   | Zone identifier        |
| Borough      | Borough name           |
| Zone         | Zone name              |
| service_zone | Service classification |


This dataset is modeled as a dimension table in Silver.

---

### 5. Dimension Modeling - SCD Type 2

#### 5.1 Dimension Table: dim_taxi_zone

The lookup dataset is implemented as a Slowly Changing Dimension Type 2 to maintain historical correctness.

#### Schema

| Column               | Description            |
| -------------------- | ---------------------- |
| zone_sk              | Surrogate key          |
| location_id          | Natural key            |
| borough              | Borough name           |
| zone                 | Zone name              |
| service_zone         | Service classification |
| effective_start_date | Record validity start  |
| effective_end_date   | Record validity end    |
| is_current           | Active record flag     |


---

#### 5.2 SCD Type 2 Behavior

When a change is detected in zone attributes:

1. The existing active record:
        - Updates `effective_end_date`
        - Sets `is_current = false`
2. A new record is inserted:
        - New surrogate key
        - Updated attribute values
        - New `effective_start_date`
        - `is_current = true`


---

#### 5.3  Why SCD Type 2?

Even if changes are rare, this approach ensures:
- Historical reporting accuracy
- Temporal analytics capability
- Enterprise-grade correctness
- Regulatory-compliant modeling patterns

This mirrors real-world enterprise warehouse design.

---

### 6. Fact-Dimension Relationships

The fact table references dimension tables using natural keys:
- pickup_location_id -> dim_taxi_zone.location_id
- dropoff_location_id -> dim_taxi_zone.location_id

Advanced implementations may use surrogate keys with temporal joins for full historical alignment.

---

### 7. Incremental Processing Strategy

#### 7.1 Fact Table
- Process only newly arrived Bronze partitions
- Standardize schemas
- Union Green and Yellow datasets
- Write using partition overwrite strategy

No full-table reloads.


#### 7.2 Dimension Table
- Detect changes using attribute-level hash comparison
- Use Delta Lake MERGE for upserts
- Maintain SCD Type 2 semantics
- Ensure only one active record per natural key

---

### 8. Scalability & Production Considerations

The Silver layer is designed to scale:

- Partitioned fact table by year and month
- Avoid full rewrites
- Use Delta MERGE for efficient dimension updates
- Enable schema evolution
- Prepare for compaction and OPTIMIZE operationsd (future enhancement)

This architecture supports:

- Multi-year ingestion
- Additional taxi datasets
- External enrichment datasets
- Migration to cloud storage (ADLS / GCS)

---

### 9. Data Quality Enforcement

The Silver layer enforces data validation rules:

- Valid pickup and dropoff timestamps
- Positive trip distance
- Non-negative fare values
- Optional referential integrity checks against dimensions

Silver ensures correctness before Gold aggregation.

---

#### 10. Gold Layer Readiness

With this design, Gold can easily compute:

- Revenue comparison (Green vs Yellow)
- Borough-level revenue performance
- Daily / Monthly KPIs
- Trip volume trends
- AI-driven natural language querying over unified fact model

Silver enables cross-dataset analytics without complexity in Gold.

---

### 11. Industry Alignment

This desing reflects enterprise data warehouse standards:
- Fact + Dimension modeling
- Surrogate key strategy
- SCD Type 2 implementation
- Multi-source unification
- Incremental ingestion design
- Separation of ingestion, transformation, and aggregation layers.

This elevates the project from a pipeline to a dimensional analytics platform.

---

### 12. Implementation Roadmap

1. Standardize Green schema
2. Standardize Yellow schema
3. Create unified fact_taxi_trips
4. Ingest and stage lookup dataset
5. Implement SCD Type 2 merge logic
6. Validate joins and data integrity
7. Prepare Gold layer KPIs

---

### Final Vision

The Silver layer becomes:
- Clean
- Unified
- Dimensional
- Historically accurate
- Incremental
- Enterprise-ready

This is the structural foundation of a scalable, production-grade data platform