# 🚕 NYC Taxi Analytics Platform
## Databricks Lakehouse Data Engineering Project

---

### 📌 Project Overview
The NYC Taxi Analytics Platform is an end-to-end Data Engineering project built using the Databricks Lakehouse architecture.
It ingests raw NYC Taxi trip data, applies scalable data transformations, and produces business-ready analytics tables to support revenue, demand, customer behavior, and operational efficiency analysis.

This project demonstrates real-world data engineering best practices, including medallion architecture, Delta Lake optimization, data quality enforcement, and KPI-driven design.

---

### 🎯 Business Objective
NYC Taxi trip data contains millions of records with valuable insights into:
- City mobility patterns
- Revenue and pricing trends
- Customer tipping behavior
- Operational inefficiencies

The goal of this project is to build a reliable analytics platform that transform raw trip data into consistent, reusable business metrics for analytics and reporting teams.

---

### Target Stakeholders
- Data Engineers
- Analytics/BI Teams
- Operations Teams
- Revenue & Pricing Analysts
- City Mobility Planners

---

### Architecture Overview
The platform follows the Databricks Lakehouse Medallion Architecture:
```
Raw NYC Taxi Data
        ↓
Bronze Layer (Raw, Immutable)
        ↓
Silver Layer (Cleaned & Enriched)
        ↓
Gold Layer (Aggregated Business Metrics)
        ↓
Databricks SQL / BI Dashboards
```

#### Why Lakehouse?
- Combines scalability of data lakes with reliability of data warehouses
- ACID transactions via Delta Lake
- Optimized for both batch processing and analytics

---

### 🧱 Data Layers Explained
#### 🟤 Bronze Layer - Raw Ingestion
- Stores raw taxi trip data as-is
- Append-only, immutable
- Enables reprocessing and auditability

#### ⚪ Silver Layer - Cleaned & Enriched
- Filter invalid records
- Normalize data types
- Adds derived fields (trip duration, total amount)
- Enriches with pickup/drop-off zone names

#### 🟡 Gold Layer - Business Metrics
- Aggregated, analytics-ready tables
- Optimized for SQL and BI tools
- Single source of truth for KPIs

---

### Business Metrics Delivered
#### Revenue Metrics
- Total Revenue
- Revenue by Pickup Zone
- Revenue by Time(hour/day/month)
- Average Fare per Trip

#### Demand & Trip Metrics
- Total Trips
- Trips by Zone
- Trips by Hour (Peak Demand)
- Average Trip Distance
- Average Trip Duration

#### Customer Behavior Metrics
- Average Tip Percentage
- Tip Distribution by Zone
- Payment Method Usage (Cash vs Card)

#### Operational Efficiency Metrics
- Revenue per Mile
- Revenue per Minute
- Short Low-Fare Trip Indicators

---

### 📐 Data Model Summary
| Layer  | Table Examples          | Grain                  |
| ------ | ----------------------- | ---------------------- |
| Bronze | `bronze_nyc_taxi_trips` | One row per trip       |
| Silver | `silver_nyc_taxi_trips` | One row per valid trip |
| Gold   | `gold_revenue_metrics`  | Date + Pickup Zone     |
| Gold   | `gold_trip_metrics`     | Date + Hour + Zone     |

---

## Architecture & Design


## Architecture & Design

- [Landing Zone Design](docs/landing-zone.md)
- [Bronze Layer Design](docs/bronze-layer.md)
- [Silver Layer Design](docs/silver-layer.md)
- [Silver Implementation](docs/silver-implementation.md)


---
### 📁 Repository Structure
```pgsql
nyc-taxi-analytics-platform/
│
├── README.md
│
├── docs/
│   ├── business-requirements.md
│   ├── metrics-definition.md
│   ├── data-model.md
│   └── data-architecture.md
│
├── notebooks/
│   ├── bronze/
│   │   └── ingest_nyc_taxi.py
│   ├── silver/
│   │   └── transform_clean_trips.py
│   └── gold/
│       └── build_business_metrics.py
│
├── sql/
│   ├── gold_metrics.sql
│   └── validation_queries.sql
│
├── tests/
│   └── data_quality_checks.py
│
└── config/
    └── pipeline_config.yaml
```

---

### Data Quality & Validation
Data quality checks are enforced in the Silver layer, including:
- Valid pickup and drop-off timestamps
- Non-negative fares and distances
- Valid payment types
- Positive trip duration

Invalid records are excluded from Gold metrics to ensure trusted analytics

---

### Technologies Used
- Apache Spark (PySpark)
- JupyterLab
- Python
- SQL
- Parquet / Delta-compatible layout
- Medallion Architecture

---

### 🚀 Future Enhancements

- Migration to Databricks Lakehouse
- Delta Lake optimizations
- Incremental ingestion
- BI dashboards (Power BI / Databricks SQL)
- Streaming ingestion

---

### This project demonstrates:

- Spark-based data engineering expertise
- Lakehouse and Medallion architecture design
- Business-driven data modeling
- Production-ready pipeline thinking
- Tool-agnostic engineering mindset

---

### 🧠 Author

Chirag Venkateshaiah
Aspiring Data Engineer | Apache Spark | Lakehouse Architecture