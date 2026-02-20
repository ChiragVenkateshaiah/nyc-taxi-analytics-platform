# Bronze Layer Implementation (Green & Yellow)

## NYC Taxi Analytics Platform

---

### 1. Overview

This document describes the implementation of the Bronze ingestion pipeline supporting both Green and Yellow taxi datasets.

The ingestion logic is reusable, dataset-agnostic, and designed for incremental processing using Delta Lake.

---

### 2. Environment Setup

The Bronze layer runs locally using:

- Conda-based PySpark environment
- Open-source Delta Lake
- Custom Spark session utility (`get_spark_session()`)
- Hadoop configuration setup (`complete_hadoop_setup()`)

Spark session is initialized before ingestion begins.

---

### 3. Configuration

#### Project Paths
```bash
data/landing/nyc_taxi
data/bronze/nyc_taxi
data/_processed_files
```

#### Taxi Types Processed
```python
TAXI_TYPES = ["green", "yellow"]
```
#### Batch ID
Each run generates a unique batch identifier:

```bash
batch_YYYYMMDD_HHMMSS
```

---

### 4. Processed Files Tracker

A Delta table tracks processed source files.

#### Behavior
- Attempts to load existing tracker
- If missing, creates new empty Delta table
- Stores file_path and processed_at timestamp

This ensures file-level incremental ingestion

---

### 5. Ingestion Flow Per Dataset

For each taxi type:

#### Step 1 - Validate Landing Directory
- Ensure taxi folder exists
- Ensure year directory (2025) exists
- Detect non-empty Parquet files

#### Step 2 - Read Data
- Uses `mergeSchema = true`
- Reads year-level partition
- Logs file sizes and row counts

#### Step 3 - Incremental Filter
- Adds `-source_file` column
- Filters out previously processed files

#### Step 4 - Add Audit Metadata

Adds:
- `_ingestion_date`
- `_ingestion_timestamp`
- `BATCH_ID`

#### Step 5 - Write Processed Files Tracker
- Extract distinct source files
- Append to `_processed_files` Delta table

---

### 6. Execution Pattern
The pipeline executes ingestion for each taxi type using wrapper functions:
```python
ingest_green_to_bronze()
ingest_yellow_to_bronze()
```
Execution results are logged and summarized at the end of the run.

---

### 7. Error Handling

The implementation includes:
- Graceful handling of missing directories
- Validation of file existence and size
- Try/except protection during Spark reads
- Safe tracker table initialization
- Summary report per dataset

Failure in one dataset do not corrupt others.

---

### 8. Design Strengths
- Dataset-agnostic ingestion function
- Idempotent processing
- File-level incremental tracking
- Metadata-driven auditability
- Extensible to additional taxi types

---

### 9. Future Enhancements
- Partition-based incremental processing
- Dynamic year detection
- Performance optimizations (compaction, optimization)
- Integration with orchestrators (Airflow/ADF)

---

### 10. Summary

The Bronze implementation now supports both Green and Yellow taxi datasets using:

- Reusable ingestion functions
- Delta Lake append-only storage
- File-level incremental processing
- Robust logging and error handling

This completes a production-aligned multi-dataset Bronze ingestion pipeline.
