# Chicago Taxi Data Engineering Pipeline

## 📌 Project Overview
An end-to-end data engineering pipeline built using **Databricks, PySpark, Delta Lake, and dbt** to transform raw Chicago taxi trip data into an **analytics-ready data warehouse**.

This project implements a **Medallion Architecture (Bronze, Silver, Gold layers)** and includes **Slowly Changing Dimension Type 2 (SCD Type 2)** for historical tracking along with data modeling for analytics and financial reconciliation use cases.

---

## 📌 Problem Statement
Raw Chicago taxi trip data was not analytics-ready due to multiple data quality and modeling issues, including:
- Duplicate records generated during joins
- Inconsistent schema across datasets
- Presence of null and missing values
- Lack of historical tracking for dimension changes
- No validation across transformation layers

This pipeline addresses these challenges by building a structured and reliable Lakehouse architecture, ensuring clean, consistent, and analytics-ready data.

---

## 📌 Architecture & Data Flow

### Ingestion Layer (Bronze)
Raw CSV datasets are ingested into Delta tables using **Databricks Auto Loader**, ensuring efficient incremental ingestion and full data lineage tracking.

### Processing Layer (Silver)
Data is processed using **PySpark**, where cleaning, schema enforcement, and transformations are performed. Row-level deduplication is handled using **window functions (row_number)**.

### Modeling Layer (Gold)
A **star schema** is built using **dbt**, transforming the cleaned data into analytics-ready models. This layer includes **SCD Type 2 logic** and **point-in-time joins** for historical tracking and analytics.

---

## 📌 Project Structure

```text
├── models/
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── snapshots/       # SCD Type 2 historical tracking
├── macros/          # Reusable dbt logic functions
├── assets/          # Lineage graphs and output screenshots
└── dbt_project.yml  # Main configuration file
```

---

## 📌 Notes
- Data quality validation was performed using custom SQL audit scripts in Databricks.
- Raw Bronze layer data and Delta tables are stored in Databricks and are not included in this repository.

---

## 📌 Key Engineering Achievements

### 🧩 Data Deduplication & Grain Fix
- **Root cause:** Identified a mismatch in join grain across fact and dimension datasets leading to row inflation.
- **Solution:** Implemented `row_number()` window function to enforce uniqueness at the correct business grain.
- **Result:** Accurate trip-level dataset with consistent row counts across all pipeline layers.

### 💰 Data Reconciliation & Financial Consistency
- **Validation:** Built SQL audit checks in Databricks to compare aggregated metrics across Silver and Gold layers.
- **Result:** Final validation confirmed accurate revenue total of **$51,122.35**, proving pipeline correctness and zero data loss.

### ⚠️ Unknown Join Skew Resolution (Revenue Attribution Fix)
- **Problem:** Resolved an issue where ~$41K revenue was incorrectly attributed to "Unknown" categories.
- **Root Cause:** Late-arriving dimension data and missing historical snapshots.
- **Solution:** Implemented **beginning-of-time fallback strategy** (1900-01-01) to ensure every trip had a valid dimension record for joins.
- **Result:** Achieved 100% revenue attribution accuracy.

### ⏱ Point-in-Time Join Modeling
- **Problem:** Standard joins failed to reflect the historical state of drivers/vehicles at the time of transaction.
- **Solution:** Implemented **point-in-time join logic** using dbt + SCD Type 2 snapshots.
- **Result:** Each trip links to the exact dimension version active at the time of the event, ensuring a single source of truth.

---

## 📌 Data Model (Star Schema)

**Fact Table:**
- `fact_trips`

**Dimension Tables:**
- `dim_drivers`
- `dim_vehicles`
- `dim_customers`
- `dim_locations`
- `dim_payments`

---

## 📊 Validation & Reconciliation

### 🔍 Summary
- **Fact Table Grain:** 1 row = 1 trip
- **Total Records Validated:** 1,000
- **Revenue Consistency Confirmed:** $51,122.35

### ✅ Layer-wise Audit

| Layer | Total Records | Total Revenue | Status |
| :--- | :--- | :--- | :--- |
| Silver (Source) | 1,000 | $51,122.35 | ✅ PASS |
| Gold (Target) | 1,000 | $51,122.35 | ✅ PASS |

---

## 📌 How to Run

1. **Bronze Layer:** Run the Bronze ingestion notebook in Databricks to load raw data.
2. **Silver Layer:** Run the Silver transformation notebook for cleaning and deduplication.
3. **Snapshot Layer:** Capture historical changes:
   ```bash
   dbt snapshot
   ```
4. **Gold Layer:** Build the Star Schema:
   ```bash
   dbt run
   ```
5. **Validation:** Run reconciliation queries in Databricks to verify revenue consistency.

---

## 📌 Future Enhancements
- Integrate **Databricks Workflows** for end-to-end orchestration.
- Implement **CI/CD** using GitHub Actions to automate dbt testing.
- Migrate manual validation queries to an automated **dbt testing framework**.
- Build a **Power BI/Tableau** dashboard on top of the Gold layer.
