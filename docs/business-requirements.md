# 📄 Business Requirement Document
## NYC Taxi Analytics Platform (Databricks Lakehouse)
---

### 1. Project Overview
Project Name
NYC Taxi Analytics Platform

#### Objective
To design and implement an end-to-end analytics platform using the Databricks Lakehouse architecture that processes NYC Taxi trip data and delivers reliable, scalable, and business-ready mobility insights.

This platform will support analytical use cases related to revenue analysis, demand forecasting, customer behavior, and operational efficiency.

---

### 2. Business Problem Statement
NYC Taxi operations generate millions of trip records containing valuable insights related to city mobility, revenue trends, and service efficiency.

However, raw taxi data:
- Is large-scale and semi-structured
- Contains missing, inconsistent, and noisy values
- Is not analytics-ready for business users

The business needs a **centralized**, optimized analytics layer that enables:
- Fast SQL-based analysis
- Consistent KPIs across teams
- Scalable processing of historical and incremental data

---

### 3. Stakeholders

| Role                  | Responsibility                                          |
| --------------------- | ------------------------------------------------------- |
| Data Engineering Team | Build and maintain ingestion & transformation pipelines |
| Analytics / BI Team   | Consume Gold tables for reporting                       |
| Operations Team       | Analyze trip efficiency and demand                      |
| Revenue Team          | Track revenue and pricing patterns                      |
| City Planning Team    | Understand mobility trends                              |

---

### 4. Data Source
#### Primary Dataset
NYC Taxi Trip Records

#### Data Characteristics
- Large volume (millions of rows)
- Time-series based
- Zone-based pickup and drop-off locations
- Contains fare, distance, duration, payment, and trip details

 #### Key Raw Attributes
 - pickup_datetime
 - dropoff_datetime
 - pickup_location_id
 - dropoff_location_id
 - trip_distance
 - fare_amount
 - tip_amount
 - tolls_amount
 - payment_type
 - passesnger_count

### 5. Solution Architecture (Databricks Lakehouse)
The solution follows the Medallion Architecture:

#### Bronze Layer (Raw)
- Stores raw ingested taxi data
- Schema-on-read
- Immutable, append-only
- Used for reprocessing and audit

#### Silver Layer (Cleaned & Enriched)
- Data cleansing (nulls, invalid values)
- Data type normalization
- Derived columns:
    - trip_duration_minutes
    - total_amount
- Zone enrichment using lookup tables

#### Gold Layer (Business Metrics)
- Aggregated, analytics-ready tables
- Optimized for BI and SQL queries
- Directly consumed by dashboards and analysts

---

### 6. Business Metrics (Gold Layer Requirements)
#### Revenue Metrics
| Metric                 | Definition                                   |
| ---------------------- | -------------------------------------------- |
| Total Revenue          | SUM(fare_amount + tip_amount + tolls_amount) |
| Revenue by Pickup Zone | Revenue grouped by pickup zone               |
| Revenue by Time        | Hourly, daily, monthly revenue               |
| Average Fare           | Avg fare per trip                            |

#### Demand & Trip Metrics
| Metric            | Definition              |
| ----------------- | ----------------------- |
| Total Trips       | Count of trips          |
| Trips by Zone     | Pickup hotspot analysis |
| Trips by Hour     | Peak demand hours       |
| Avg Trip Distance | Mean distance per trip  |
| Avg Trip Duration | Mean duration per trip  |

#### Customer Behavior Metrics
| Metric                      | Definition                 |
| --------------------------- | -------------------------- |
| Avg Tip Percentage          | (tip / fare) * 100         |
| Tip by Zone                 | Zone-wise tipping patterns |
| Payment Method Distribution | % of each payment type     |

#### Operational Efficiency Metrics
| Metric               | Definition                     |
| -------------------- | ------------------------------ |
| Revenue per Mile     | Total revenue / total miles    |
| Revenue per Minute   | Total revenue / total duration |
| Low Fare Short Trips | Indicator of inefficiency      |

---

### 7. Non-Functional Requirements
#### Performance
- Queries on Gold tables must be optimized for BI tools
- Partitioning on date columns

#### Scalability
- Support multi-year historical data
- Incremental ingestion support

#### Reliability
- Data quality checks at Silver layer
- Ability to reprocess from Bronze

#### Maintainability
- Modular notebook structure
- Config-driven pipelines

---

### 8. Out of Scope (Phase 1)
- Real-time streaming ingestion
- Machine learning models
- Fare prediction
- Rider/driver behavioral modeling

(These can be future enhancements)

---

### 9. Success Criteria
The project is considered successful if:
- Business metrics are reproducible and consistent
- Gold tables are consumable via Databricks SQL
- Pipelines are modular and re-runnable
- Project demonstrates production-grade IDE best practices

### 10. This Project demonstrates:
- Lakehouse architecture mastery
- Business-first data engineering
- KPI-driven pipeline design
- Databricks production patterns


