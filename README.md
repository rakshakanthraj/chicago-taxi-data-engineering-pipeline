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
