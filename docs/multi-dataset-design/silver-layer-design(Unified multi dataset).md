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

