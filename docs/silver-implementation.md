# 🥈 Silver Layer Implementation
## NYC Taxi Analytics Platform

---
### 1. Objective
The Silver layer transforms structured Bronze data into clean, validated, and analytics-ready Delta tables.

This implementation focuses intentionally on:
- ✅ NYC Green Taxi data
- ✅ A limited time window (single month initially)
- ✅ Mastering PySpark transformations and Delta operations
- ✅ Building correctness before scaling volume

The logic is designed to scale to additional months and taxi types without structural redesign.

---

### 2. Input Source
- Upstream Layer: Bronze
- Format: Delta Lake
- Path:
  ```bash
  data/bronze/nyc_taxi/green/
  ```

Bronze data contains:
- Raw source schema
- Ingestion metadata columns
- No data quality enforcement

---

### 3. Output Destination
- Layer: Silver
- Format: Delta Lake
- Path:
  ```bash
  data/silver/nyc_taxi/green/
  ```

The Silver table is:
- Partitioned by `year` and `month`
- Cleaned and standardized
- Suitable for downstream aggregations (Gold layer)

---

### 4. Transformation Steps
#### 4.1 Column Selection & Standardization
Columns are explicitly selected and renamed to enforce consistent naming conventions:
```text
Bronze Column	          Silver Column
VendorID	                vendor_id
lpep_pickup_datetime	    pickup_ts
lpep_dropoff_datetime	    dropoff_ts
```

This ensures consistent schema design and simplifies downstream SQL.

#### 4.2 Data Quality Rules
Conservative validation rules are applied:
- `pickup_ts IS NOT NULL`
- `dropoff_ts IS NOT NULL`
- `trip_distance > 0`
- `fare_amount >=0`
- `total_amount >= fare_amount`

Records failing these rules are filtered out.

> No silent correction is performed -- invalid records are excluded.

#### 4.3 Data Visibility & Validation
Before writing to Silver:
- Total record count is calculated
- Valid record count is calculated
- Dropped record count in logged

This ensures transperency and debuggability.

#### 4.4 Derived Columns (Partition Strategy)
The following columns are derived from `pickup_ts`:
- `year`
- `month`

These columns are used for partitioning the Silver Delta table.
Partitioning enables:
- Efficiency query pruning
- Scalable data growth
- Optimized aggregations

---

### 5. Write Strategy
The Silver layer currently uses:
```bash
.mode("overwrite")
.partitionBy("year", "month")
```
Overwrite mode is used during the learning phase for simplicity.

In a production scenario, this would transition to:
- Partition-level overwrite
- Or incremental append logic

---
### 6. Responsibility of Silver Layer
The Silver layer:
- Cleans and validates Bronze data
- Standardizes schema
- Derives analytical partition columns
- Produces trusted Delta tables

The Silver layer does NOT:
- Perform aggregations
- Compute KPIs
- Apply heavy business logic
- Create BI-ready summaries

These responsibilities belong to the Gold layer.

---
### 7. Scalability Considerations
Although currently limited to one month of Green Taxi data, the implementation:
- Supports additional months without structural changes
- Can be extended to Yellow taxi by reusing logic
- Supports schema evolution through Delta Lake
- Is compatible with incremental Bronze ingestion

The architecture prioritizes correctness first, scale second.

---

### 8. Summary
The Silver implementation achieves:
- Clean and validated taxi trip records
- Transparent data quality enforcement
- Partitioned Delta storage
- Clear separation from ingestion logic

This layer bridges raw ingestion (Bronze) and business analytics (Gold), providing a trustworthy foundation for metric computation and reporting.
