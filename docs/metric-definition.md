# 📊 Metrics Definition Document
## NYC Taxi Analytics Platform (Databricks Lakehouse)

---

### 1. Purpose of This Document
This document defines business metrics at column-level precision to ensure:
- A single source of truth for KPIs
- Consistent reporting across teams
- Clear mapping between Gold tables and business questions

All metrics defined here are implemented in the Gold Layer and consumed by Databricks SQL/Bi tools.

---

### 2. Gold Layer Design Principles
- Grain-first design (clearly defined aggregation level)
- Metrics are pre-aggregated
- Optimized for read-heavy analytics
- No raw or semi-clean data exposed

---

### 3. Gold Tables Overview
| Gold Table                | Grain                   | Purpose                |
| ------------------------- | ----------------------- | ---------------------- |
| `gold_revenue_metrics`    | date, pickup_zone       | Revenue analysis       |
| `gold_trip_metrics`       | date, hour, pickup_zone | Demand & trip analysis |
| `gold_customer_metrics`   | date, pickup_zone       | Customer behavior      |
| `gold_efficiency_metrics` | date, pickup_zone       | Operational efficiency |

---

### 4. Revenue Metrics
#### Gold Table: `gold_revenue_metrics`
Grain:
> One row per date + pickup_zone

| Column Name   | Data Type | Definition        | Source / Logic                                 |
| ------------- | --------- | ----------------- | ---------------------------------------------- |
| trip_date     | DATE      | Trip pickup date  | `DATE(pickup_datetime)`                        |
| pickup_zone   | STRING    | Pickup zone name  | Zone lookup                                    |
| total_revenue | DECIMAL   | Total revenue     | `SUM(fare_amount + tip_amount + tolls_amount)` |
| fare_revenue  | DECIMAL   | Fare-only revenue | `SUM(fare_amount)`                             |
| tip_revenue   | DECIMAL   | Tip-only revenue  | `SUM(tip_amount)`                              |
| total_trips   | BIGINT    | Number of trips   | `COUNT(*)`                                     |
| avg_fare      | DECIMAL   | Avg fare per trip | `AVG(fare_amount)`                             |

---

### 5. Trip & Demand Metrics
#### Gold Table: `gold_trip_metrics`
Grain:
> One row per date + hour + pickup_zone

| Column Name           | Data Type | Definition              | Source / Logic               |
| --------------------- | --------- | ----------------------- | ---------------------------- |
| trip_date             | DATE      | Pickup date             | `DATE(pickup_datetime)`      |
| trip_hour             | INT       | Pickup hour             | `HOUR(pickup_datetime)`      |
| pickup_zone           | STRING    | Pickup zone             | Zone lookup                  |
| total_trips           | BIGINT    | Trips count             | `COUNT(*)`                   |
| avg_trip_distance     | DECIMAL   | Avg trip distance       | `AVG(trip_distance)`         |
| avg_trip_duration_min | DECIMAL   | Avg trip duration (min) | `AVG(trip_duration_minutes)` |

---

### 6. Customer Behavior Metrics
#### Gold Table: `gold_customer_metrics`
Grain:
> One row per date + pickup_zone

| Column Name        | Data Type | Definition  | Source / Logic                                  |
| ------------------ | --------- | ----------- | ----------------------------------------------- |
| trip_date          | DATE      | Pickup date | Derived                                         |
| pickup_zone        | STRING    | Pickup zone | Lookup                                          |
| avg_tip_percentage | DECIMAL   | Avg tip %   | `AVG((tip_amount / fare_amount) * 100)`         |
| cash_payments      | BIGINT    | Cash trips  | `SUM(CASE WHEN payment_type='Cash' THEN 1 END)` |
| card_payments      | BIGINT    | Card trips  | `SUM(CASE WHEN payment_type='Card' THEN 1 END)` |
| total_payments     | BIGINT    | Total trips | `COUNT(*)`                                      |

---

### 7. Operational Efficiency Metrics
#### Gold Table: `gold_efficiency_metrics`
Grain:
> One row per date + pickup_zone

| Column Name          | Data Type | Definition         | Source / Logic                                              |
| -------------------- | --------- | ------------------ | ----------------------------------------------------------- |
| trip_date            | DATE      | Pickup date        | Derived                                                     |
| pickup_zone          | STRING    | Pickup zone        | Lookup                                                      |
| revenue_per_mile     | DECIMAL   | Revenue efficiency | `SUM(total_amount) / SUM(trip_distance)`                    |
| revenue_per_minute   | DECIMAL   | Time efficiency    | `SUM(total_amount) / SUM(trip_duration_minutes)`            |
| short_low_fare_trips | BIGINT    | Inefficient trips  | `COUNT WHERE trip_distance < 1 AND fare_amount < threshold` |

---

### 8. Metric Validation Rules
#### Data Quality Checks (Silver -> Gold)
- `fare_amount >= 0`
- `trip_distance > 0`
- `pickup_datetime < dropoff_datetime`
- `trip_duration_minutes > 0`
- `payment_type IS NOT NULL`

Records failing checks are exluded from Gold metrics.

---

### 9. Business Questions -> Metrics Mapping
| Business Question                  | Gold Table                |
| ---------------------------------- | ------------------------- |
| Which zones generate most revenue? | `gold_revenue_metrics`    |
| When is demand highest?            | `gold_trip_metrics`       |
| Where do customers tip more?       | `gold_customer_metrics`   |
| Which trips are inefficient?       | `gold_efficiency_metrics` |


---

### 10. Change Management
- New metrics require updates to this document
- Backward compatibility maintained via versioned tables
- Schema evolution handled using Delta Lake

