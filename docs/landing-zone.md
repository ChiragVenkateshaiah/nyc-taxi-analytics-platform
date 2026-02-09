# Landing Zone Design
## NYC Taxi Analytics Platform

---

### 1. Purpose of the Landing Zone
The Landing Zone is the first entry point for data into the NYC Taxi Analytics Platform. Its primary purpose is to store raw source data exactly as received, without any transformation, enrichment, or schema enforcement.

The landing zone acts as:
- An immutable backup of source data
- A replayable source for downstream layers
- A safety net for reprocessing and debugging

> Core principle: *What the source sends is what we store*.

---

### 2. Why a Landing Zone is Used
Although a NYC Taxi data is publicly avaiable, a landing zone is intentionally introduced to mirror real-world enterprise data platforms.

Key reasons:
- Preserves original source files for audit and lineage
- Enables full reprocessing if downstream logic changes
- Decouples source ingestion from transformation logic
- Aligns with Medallion/Lakehouse architecture practices

This design closely reflects how data is ingested in production systems using cloud object storage (ADLS, S3, GCS)

---

### 3. Design Principles
The landing zone follows these strict rules:
- Append-only: Existing files are never modified or overwritten
- No transformations: No schema changes, filtering, or enrichment
- Original format preserved: Files are stored as Parquet, exactly as received
- Read-only downstream: Only bronze ingestion jobs read from landing
- Idempotent ingestion: Re-running the job does not duplicate data

The landing zone is intentionally kept lighweight and simple.

---

### 4. Data Source
- Source: NYC TLC Trip Records
- Access Method: Public CloudFront endpoint
- Base URL:
  > https://d37ci6vzurychx.cloudfront.net/trip-data

All taxi datasets (yellow,green, etc) are accessed by dynamically constructing file names against this base URL

---

### 5. Folder Structure
The landing zone is organized by domain - dataset - temporal partitions
```text
data/landing/nyc_taxi/
├── yellow/
│ └── year=2024/
│ └── month=01/
│ └── yellow_tripdata_2024-01.parquet
├── green/
│ └── year=2024/
│ └── month=01/
│ └── green_tripdata_2024-01.parquet
```
#### Benefits of This Structure
- Clear separation by taxi type
- Easy backfills and reprocessing
- Natural partitioning for downstream Spark jobs
- Cloud-storage friendly layout

---

### 6. Ingestion Strategy
Landing zone ingestion is implemented using pure Python, without Spark.

#### Ingestion Characteristics
- Files are downloaded directly from the source endpoint
- Each files is checked for existence before download
- Already ingested files are skipped
- Missing or unpublished months are handled gracefuly

This ensures the ingestion process is incremental and idempotent.

---

### 7. Incremental Logic
Incrementally is enforced at the file level.

Logic:
1. Construct file name based on taxi type, year and month
2. Check if the file already exists in the landing zone
3. if it exists -> skip
4. If it does not exist -> download and store

This approach guarantees:
- No duplicate files
- Safe re-runs
- Predictable ingestion behavior

---

### 8. What the Landind Zone Does NOT Do
The following responsibilities are explicitly excluded from the landing zone:
- Schema enforcement
- Data validation
- Deduplication
- Metadata enrichment
- Delta table creation
- Business logic application

All such processing is deferred to the Bronze layer.

---

### 9. Relationship to Bronze Layer
The landing zone serves as the upstream source for Bronze ingestion.
- Bronze jobs read only from landing
- Bronze tables are created in Delta format
- Ingestion metadata is added in Bronze, not in landing

This separation ensures clear responsibility boundaries and simplifies pipeline evolution.

---

### 10. Summary
The landing zone provides a robust and enterprise-aligned foundation for the NYC Taxi Analytics Platform by:
- Preserving raw source data immutably
- Enabling safe reprocessing and debugging
- Decoupling ingestion from transformation
- Supporting scalable and maintainable pipelines

This design intentionally mirrors real-world data engineering practices and prepares the platform for future expansion.