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

This pipeline addresses these challenges by building a **structured and reliable Lakehouse architecture**, ensuring clean, consistent, and analytics-ready data for downstream reporting and analysis.

---

## 📌 Architecture & Data Flow

### Ingestion Layer (Bronze)
Raw CSV datasets are ingested into **Delta tables** using **Databricks Auto Loader**, ensuring efficient incremental ingestion and full data lineage tracking.

### Processing Layer (Silver)
Data is processed using **PySpark**, where cleaning, schema enforcement, and transformations are performed. Row-level deduplication is handled using **window functions (row_number)**.

### Modeling Layer (Gold)
A **star schema** is built using **dbt**, transforming the cleaned data into analytics-ready models. This layer includes **SCD Type 2 logic** and **point-in-time joins** for historical tracking and analytics.

## 📌 Project Structure

### models/
- staging/
- intermediate/
- marts/

### snapshots/
Used for implementing **SCD Type 2 (historical tracking of dimension changes)** using dbt snapshots.

### macros/
Contains a small number of reusable dbt logic functions used in transformations.

### assets/
- Lineage graphs  
- Pipeline architecture diagrams  
- Output screenshots  

### dbt_project.yml
Main configuration file for the dbt project.

---

## 📌 Notes
- Data quality checks were performed in **Databricks using SQL queries**
- Data quality validation was performed using custom SQL audit scripts in Databricks to ensure cross-layer financial       reconciliation.
- Raw (Bronze layer) data and Delta tables exist in Databricks and are not part of the GitHub repository

## 📌 Key Engineering Achievements

### 🧩 Data Deduplication & Grain Fix
Identified a row duplication issue caused by incorrect join logic between fact and dimension tables, leading to row inflation at the trip level.

- Root cause: mismatch in join grain across fact and dimension datasets  
- Implemented **row_number window function** to enforce uniqueness at the correct business grain  
- Resulted in accurate trip-level dataset with consistent row counts across all pipeline layers  

---

### 💰 Data Reconciliation & Financial Consistency
Built validation checks using SQL queries in Databricks to compare aggregated metrics across Silver and Gold layers.

- Detected and verified consistency in revenue calculations after transformations  
- Ensured no data loss or duplication during modeling stages  
- Final validation confirmed accurate revenue total of **$51,122.35**, proving pipeline correctness  

---

### ⚠️ Unknown Join Skew Resolution (Revenue Attribution Fix)
Resolved a major data issue where approximately **$41K revenue was incorrectly attributed to "Unknown" category**.

- Root cause: late-arriving dimension data and missing historical snapshots  
- Implemented **beginning-of-time fallback strategy** to ensure every trip had a valid dimension record for joins  
- Achieved 100% revenue attribution accuracy by redistributing all values to correct categories  

---

### ⏱ Point-in-Time Join Modeling
Addressed limitations of standard joins that failed to reflect historical business state at the time of each transaction.
- Example: driver or vehicle changes over time were not captured correctly  
- Implemented **point-in-time join logic using dbt + SCD Type 2 snapshots**  
- Ensured each trip is linked to the exact dimension version active at the time of the event  
- Resulted in a **single source of truth with full historical accuracy**

## 📌 Data Model (Star Schema)

Fact table is at the center of the schema and is connected to all dimension tables.

Fact Table:
- fact_trips

Dimension Tables:
- dim_drivers
- dim_vehicles
- dim_customers
- dim_locations
- dim_payments

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



  
