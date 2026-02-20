# Bronze Layer Design (Multi-Dataset)

## NYC Taxi Analytics Platform

---

### 1. Purpose
The Bronze layer is the frist structured layer in the NYC Taxi Analytics Platform. It converts raw landing-zone files into structured Delta tables while preserving the source data as closely as possible.

This version supports multiple taxi datasets (Green and Yellow) using a reusable ingestion framework.

> Core Principle: *Bronze stores raw data with structure and lineage - not business logic.

---

### 2. Supported Datasets

The Bronze layer now processes:
- NYC Green Taxi
- NYC Yellow Taxi

Each dataset is handled using the same ingestion logic but sored independently.

---

### 3. Input Source

- Upstream Layer: Landing Zone
- Format: Parquet
- Structure:

```text
data/landing/nyc_taxi/
├── green/
│   └── 2025/month=MM/*.parquet
└── yellow/
    └── 2025/month=MM/*.parquet
```
The Bronze layer never reads directly from external sources.

---

### 4. Output Structure

- Storage Format: Delta Lake
- Write Mode: Append-only

```text
data/bronze/nyc_taxi/
├── green/
└── yellow/
```
Each taxi dataset is stored independently but follows identical structural conventions.

---

### 5. Incremental Ingestion Strategy
Incrementality is enforced using a file-level tracking mechanism, similar to Auto Loader.

Processed Files Tracker
```bash
data/_processed_files
```
#### Schema
| Column Name         | Data Type | Description                            |
| ------------------- | --------- | ----------------------                 |
| file_path           | STRING    | Absolute path of processed source file |
| _processed_at       | TIMESTAMP | Ingestion timestamp                    |

---

### 6. Incremental Logic Flow

1. Discover Parquet files under landing zone
2. Filter non-empty files
3. Add `_source_file` using `input_file_name()`
4. Exclude files already recorded in `_processed_files`
5. Append new records to Bronze Delta table
6. Record processed files in tracker

This guarantees:

- Idempotency
- Safe re-runs
- No duplicate processing

---

### 7. Metadata Columns Added

| Column Name         | Data Type | Description                            |
| ------------------- | --------- | ----------------------                 |
| _source_file        | STRING    | Original landing file path             |
| _ingestion_date     | TIMESTAMP | Date of Ingestion                      |
| _ingestion_timestamp| TIMESTAMP | timestamp of ingestion                 |
| BATCH_ID            | INT       | Unique identifier for ingestion run    |

---

### 8. Responsibilities of Bronze

#### Bronze:
- Structure raw files into Delta tables
- Preserves lineage metadata
- Supports incremental ingestion

#### Bronze does NOT:
- Clean data
- Deduplicate records
- Apply business logic
- Perform aggregations

These responsibilities belong to Silver and Gold.

---

### 9. Extensibility

The ingestion logic is dataset-agnostic. Adding new taxi types requires:

- Adding a landing folder
- Adding the dataset name to TAXI_TYPES list

No redesign is required.

---

### 10. Summary

The Bronze layer now suports multi-dataset ingestion (Green & Yellow) using:
- Append-only Delta tables
- File-level incremental tracking
- Reusable ingestion functions
- Clear separation of responsibilities

This design is scalable, production-aligned, and extensible.

