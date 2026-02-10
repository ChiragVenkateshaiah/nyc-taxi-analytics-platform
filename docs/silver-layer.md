# Silver Layer Design
## NYC Taxi Analytics Platform

---

### 1. Purpose of the Silver Layer
The Silver layer is responsible for transforming Bronze data into a clean, standardized, and analytics-ready format.

While the Bronze layer focuses on structure and lineage, the Silver layer focuses on data quality and consistency.

> Core principle: Silver stores trusted, cleaned data that can be safely used for analytics and downstream aggregations

---

### 2. Position in the Architecture
```text
Landing (Raw Files)
↓
Bronze (Raw + Metadata, Delta)
↓
Silver (Cleaned, Standardized, Delta)
↓
Gold (Aggregations / Business Metrics)
```
The Silver layer always reads from Bronze and never directly from the landing zone or source systems.

---

### 3. Current Scope (Learning-First Approach)
For the initial implementation, the Silver layer will:
- Process NYC Green Taxi data only
- Work on a limited time range (single month initially)
- Focus on correctness, clarity, and spark fundamentals

This constrained scope allows deep understanding of:
- PySpark DataFrame transformations
- SQL-style data cleaning
- Performance-aware transformation patterns

The design is intentionally scalable without refactoring

---

### 4. Input Source (Bronze Layer)
- Source Format: Delta Lake
- Source Path:
  ```bash
  data/bronze/nyc_taxi/green/
  ```
- Data Characteristics:
      - Raw schema from source
      - Ingestion metadata columns
      - No data quality guarantees

---

### 5. Output (Silver Storage)
- Storage Format: Delta Lake
- Write Mode: Overwrite by partition or append (depending on strategy)
- Path:
  ```bash
  data/silver/nyc_taxi/green/
  ```

The Silver layer contains cleaned and standardized trip records that are safe for analysis.

---

### 6. Silver Layer Responsibilities
The Silver layer performs the following transformations:

#### 6.1 Data Type Normalization
- Ensure timestamps are valid and properly typed
- Cast numeric fields to appropriate data types
- Standardize string columns where needed

---

#### 6.2 Null & Invalid Data Handling
Examples:
- Remove records with null pickup or dropoff timestamps
- Filter trips with negative or zero distance
- Filter invalid fare or total amounts

These rules improve data reliability while remaining conservative.

#### 6.3 Business Rule Enforcement (Lightweight)
At Silver level, only generic sanity rules are applied:
- `trip_distance > 0`
- `fare_amount >= 0`
- `total_amount >= fare_amount`

Business-specific aggregations are deferred to Gold.

#### 6.4 Column Standardization
- Rename columns to a consistent naming convention
- Ensure consistent timestamp column names
- Drop technical-only columns not required downstream

Ingestion metadata may be retained or partially dropped depending on usage.

#### 6.5 Deduplication(If Applicable)
If duplicate records exist:
- Deduplicate using a deterministic key (e.g., pickup timestamp + location + vendor)
- Deduplication logic is explicitly defined and documented

This step is optional and data-driven

---

### 7. Incremental Processing Strategy
The Silver layer processes data incrementally based on Bronze ingestion:
- Only newly ingested Bronze data is transformed
- Partition-based processing (e.g., year/month) is preferred
- Existing Silver data is not reprocessed unnecessarily

This ensures efficient scaling as data volumne grows.

---

### 8. Partitioning Strategy
Silver tables are partitioned to support performance and scalability
- Recommended partitions:
  - `year`
  - `month`

Partition columns are derived from pickup timestamp fields.

---

### 9. Error Handling & Data Quality Visibility
- Records failing Silver rules are filtered out, not corrected
- Counts of dropped records are logged
- No silent data loss

This keeps the Silver layer transparent and debuggable.

---

### 10. What the Silver Layer Does NOT Do
The Silver layer explicitly avoids:
- Aggregations or metrics
- KPI calculations
- BI-ready summaries
- Heavy business logic

These responsibilities belong to the Gold layer.

---

### 11. Extensibility
The Silver design supports:
- Additional months with no code changes
- Yellow and other taxi datasets
- Schema evolution from Bronze
- Performance tuning as volumne increases

All transformations are reusable and modular.

---

### 12. Summary
The Silver layer provides:
- Clean, validated, and standardized taxi trip data
- A trustworthy foundation for analytics
- Clear separation from raw ingestion logic
- Scalable, incremental processing patterns

This layer bridges raw ingestion and business analytics while maintaining clarity and correctness.

