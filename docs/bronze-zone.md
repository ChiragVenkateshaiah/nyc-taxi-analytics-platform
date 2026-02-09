# Bronze Layer Design
## NYC Taxi Analytics Platform

---

### 1. Purpose of the Bronze Layer
The Bronze layer represents the first structured layer in the data platform. Its primary responsibility is to convert raw landing-zone files into structured Delta tables while preserving the data as close to the source as possible.

The Bronze layer acts as:
- A structured representation of raw source data
- An append-only, auditable data store
- The foundation for downstream Silver and Gold transformations

> Core principle: *Bronze stores raw data with structure and lineage, not business logic.*

---

### 2. Current Scope (Intentional Design Choice)
For the initial implementation:
- Only NYC Green Taxi data is processed
- Only a single month/year (2025) is ingested

This is an intentional decision, not a limitation.

#### Rationale
- Green taxi data is smaller and easier to iterate on
- Focus is placed on understanding PySpark, Delta Lake, and incremental ingestion
- The ingestion logic is designed to be easily extensible to additional months and taxi types later

Scaling to larger datasets and multiple months will reuse the same pipeline with minimal changes.

---

### 3. Input Source
- Upstream Layer: Landing Zone
- Data Format: Parquet
- Path Structure:
```bash
data/landing/nyc_taxi/green/
└── 2025/
└── month=MM/
└── green_tripdata_2025-MM.parquet
```
The Bronze layer reads only from the landing zone and never directly from the external source.

---

### 4. Output (Bronze Storage)
- Storage Format: Delta Lake
- Write Mode: Append-only
- Path:
```bash
data/bronze/nyc_taxi/green/
```
Delta Lake is used to enable:
- ACID guarantees
- Schema evolution
- Time travel (Future use)
- Reliable incremental ingestion

---

### 5. Incremental Ingestion Strategy
Incrementality in the Bronze layer is enforced using file-level tracking, similar to how Databricks Auto Loader works.

Processed Files Tracker
A dedicated Delta table tracks which source files have already been ingested:
```bash
data/bronze/_processed_files
```
#### Tracker Schema
```text
Column	Type	Description
file_path	STRING	Absolute source file path
processed_at	TIMESTAMP	Time when the file was ingested
```
---

### 6. Incremental Logic Flow
1. Read all Parquet files from the landing zone
2. Add `_source_file` column using `input_file_name()`
3. Exclude files already present in `_processed_files`
4. Process only new, unprocessed files
5. Append new data to Bronze Delta table
6. Update `_processed_files` tracker

This guarantees:
- Idempotent ingestion
- Safe re-runs
- No duplicate processing

---

### 7. Data Validation at Bronze Level
Minimal validation is applied:
- Only non-empty Parquet files are processed
- File existence and size checks are performed

No row-level data quality rules are enforced at this stage.

---

### 8. Ingestion Metadata Columns
The Bronze layer adds ingestion metadata for auditability and lineage:
```
Column	                     Description
_source_file	        Original landing file path
_ingestion_date	        Date of ingestion
_ingestion_timestamp	Timestamp of ingestion
_batch_id	            Unique identifier for the ingestion run
```
These columns enable debugging, replay, and traceability across layers.

---

### 9. What the Bronze Layer Does NOT Do
The Bronze layer intentionally avoids:
- Deduplication of records
- Data cleansing or standardization
- Business rule application
- Aggregations or joins
- Analytical transformations

All such logic is deferred to the Silver Layer.

---

### 10. Error Handling & Robustness
The ingestion notebook includes:
- Graceful handling of missing landing directories
- Validation of file availability and size
- Safe creation and reuse of the processed-files tracker
- Clear logging for ingestion progress and outcomes

Failures are isolated and do not corrupt existing Bronze data.

---

### 11. Extensibility & Future Enhancements
The current Bronze design supports easy extension:
- Additional months can be ingested by adding data to the landing zone
- Yellow and other taxi types can reuse the same logic
- Schema evolution is supported through Delta Lake
- Performance optimizations can be introduced as data volume grows

No redesign is required to scale the pipeline.

---

### 12. Summary
The Bronze layer provides a robust and scalable foundation by:
- Structuring raw landing data into Delta tables
- Enforcing incremental, idempotent ingestion
- Preserving full data lineage and audit metadata
- Remaining lightweight and transformation-free

This design prioritizes correctness, clarity, and learning, while remaining fully production-aligned
