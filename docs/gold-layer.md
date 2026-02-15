# 🥇 Gold Layer Design
## NYC Taxi Analytics Platform

---
### 1. Purpose of the Gold Layer
The Gold layer represents business-ready, aggregated datasets optimized for:
- Analytics
- Reporting
- KPI dashboards
- Decision-making
- AI assistant queries (future goal)

> Core principle: *Gold tables answer business questions directly.*

Bronze = raw
Silver = clean
Gold = insight

---
### 2. Position in Architecture
```scss
Landing (Raw Files)
      ↓
Bronze (Structured + Metadata)
      ↓
Silver (Cleaned & Standardized)
      ↓
Gold (Business Metrics & Aggregations)
```
Gold never reads from Bronze.
It only reads from Silver.

---

### 3. Current Scope (Intentional)
For Phase 1:
- ✅ Green Taxi only
- ✅ Single month (initially)
- ✅ Core revenue & trip metrics
- ✅ Aggregations-first design

We are focusing on:
- Business logic understanding
- Spark aggregations
- SQL-style transformations
- Metric modeling

Scaling to multi-month and multi-dataset is configuration-driven later.

---

### 4. Gold Layer Storage
```swift
data/gold/nyc_taxi/green/
```
Format:
- Delta Lake
- Aggregated tables
- Partitioned where meaningful

---

### 5. Business Metrics to Implement (Phase 1)
We will build three Gold tables.

---

#### Gold Table 1: Daily Trip Metrics
Table Name:
```nginx
gold_green_daily_metrics
```

Grain:
One row per date

Metrics:
- total_trips
- total_revenue (sum of total_amount)
- total_fare
- avg_trip_distance
- avg_fare_amount
- avg_total_amount

Business Questions Answered:
- What was today's total revenue?
- How many trips were completed?
- How is average fare trending?

---

#### Gold Table 2: Location-Based Revenue Metrics
(We can extend once zone lookup is added.)

##### Grain:
Pickup location (later:borough)

##### Metrics:
- total_trips_by_location
- revenue_by_location
- avg_fare_by_location

##### Business Questions:
- Which areas generate highest revenue?
- Where is demand strongest?

---

#### Gold Table 3: Hourly Demand Metrics
##### Grain:
Date + Hour

##### Metrics:
- trips_per_hour
- revenue_per_hour
- avg_fare_per_hour

##### Business Questions:
- Peak demand hours?
- Revenue spikes?
- Rush hour impact?

---

### 6. Aggregation Logic Design
All Gold tables will:
1. Read from Silver Delta
2. Group by grain (date/hour/location)
3. Aggregate using Spark SQL functions
4. Write to Delta tables
5. Use overwrite (initially)

---

### 7. Example Metric Definitions (Formal)
| Metric        | Definition         |
| ------------- | ------------------ |
| total_trips   | COUNT(*)           |
| total_revenue | SUM(total_amount)  |
| avg_fare      | AVG(fare_amount)   |
| avg_distance  | AVG(trip_distance) |

These are deterministic and auditable

---

### 8. Partitioning Strategy
Gold tables should be partitioned by:
- year
- month

Derived from pickup timestamp.

---

### 9. Incremental Strategy (Future-Ready)
Initially:
- .mode("overwrite") for learning simplicity

Production-ready pattern later:
- Overwrite by partition
- Process only new Silver partitions
- Merge-based updates (if needed)

Architecture already supports this.

---

### 10. What Gold Does NOT Do
Gold does NOT:
- Clean data (Silver did that)
- Track ingestion metadata
- Preserve raw lineage columns
- Store detailed row-level records

Gold is optimized for:
- Business consumption
- Aggregated views
- Performance

---

### 11. Why This Gold Design Is Strong
This design:
- ✔ Separate transformation from metrics
- ✔ Keeps Silver reusable
- ✔ Makes AI-assistant queries easy
- ✔ Mirrors real enterprise BI modeling
- ✔ Is extensible to multiple taxi types

