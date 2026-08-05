# Chicago Taxi Data Engineering Pipeline

## Overview

This project demonstrates an end-to-end data engineering pipeline built using **Databricks, PySpark, Delta Lake, and dbt**. It ingests raw Chicago taxi trip data, cleans and transforms it, implements **Slowly Changing Dimension (SCD Type 2)** for historical tracking, and builds an analytics-ready star schema.

---

## Project Objective

Build a production-style data engineering pipeline that processes Chicago taxi trip data using the Medallion Architecture while preserving historical dimension changes and producing validated datasets for analytics.

---

## Architecture

```text
                Raw CSV Files
                      │
                      ▼
             Bronze Layer
        Databricks Auto Loader
                      │
                      ▼
             Silver Layer
      Data Cleaning & Validation
           Deduplication
                      │
                      ▼
              Gold Layer
       dbt Star Schema Models
      SCD Type 2 Snapshots
        Point-in-Time Joins
                      │
                      ▼
       Analytics Ready Lakehouse
```

---

## Technology Stack

* Databricks
* PySpark
* Delta Lake
* dbt
* SQL
* Git

---

## Skills Demonstrated

* ETL Pipeline Development
* Medallion Architecture
* PySpark Data Processing
* Delta Lake
* Data Cleaning & Validation
* Window Functions
* Slowly Changing Dimension (SCD Type 2)
* Point-in-Time Joins
* Star Schema Modeling
* Data Reconciliation

---

## Repository Structure

```text
models/
├── staging/
├── intermediate/
└── marts/

snapshots/
macros/
assets/
dbt_project.yml
README.md
```

---

## ETL Workflow

1. Ingest raw taxi trip data into the Bronze layer.
2. Clean and validate data in the Silver layer.
3. Remove duplicate records using window functions.
4. Build dimension and fact tables.
5. Implement SCD Type 2 snapshots.
6. Perform Point-in-Time joins.
7. Generate analytics-ready Gold models.

---

## Key Features

* Automated ingestion using Databricks Auto Loader
* Data cleaning and validation
* Duplicate record handling
* Historical tracking using SCD Type 2
* Point-in-Time joins
* Star schema modeling
* Revenue reconciliation across layers

---

## Engineering Highlights

### Data Deduplication

**Problem**

Joining multiple datasets introduced duplicate trip records.

**Solution**

Used **ROW_NUMBER()** window functions to retain the correct business grain.

**Outcome**

* Fact table grain: **One row represents one trip**
* Consistent record counts across all layers

---

### Revenue Reconciliation

Built SQL validation queries to compare Silver and Gold layers.

**Validation Result**

* Total Trips: **1,000**
* Revenue: **$51,122.35**
* Zero data loss during transformation

---

### Unknown Revenue Attribution Fix

**Problem**

Approximately **$41K** revenue was incorrectly attributed to **Unknown Vehicle Type**.

**Root Cause**

Late-arriving dimension records caused trips to miss valid dimension mappings.

**Solution**

Implemented a **Beginning-of-Time (1900-01-01)** fallback strategy to ensure every trip matched the correct historical dimension record.

**Outcome**

* Eliminated incorrect Unknown mappings
* Achieved accurate revenue attribution

---

### Point-in-Time Historical Joins

Implemented historical joins using dbt snapshots.

```sql
trip_timestamp
BETWEEN valid_from
AND valid_to
```

This ensures every trip is linked to the correct historical version of the dimension.

---

## Data Model

### Fact Table

* fact_trips

### Dimension Tables

* dim_drivers
* dim_customers
* dim_locations
* dim_payments
* dim_vehicles

---

## Validation

| Layer  | Trips |    Revenue | Status |
| ------ | ----: | ---------: | ------ |
| Silver | 1,000 | $51,122.35 | PASS   |
| Gold   | 1,000 | $51,122.35 | PASS   |

---

## Prerequisites

* Python 3.8+
* Apache Spark 3.x
* Databricks
* dbt
* Git

---

## Running the Project

Clone the repository:

```bash
git clone https://github.com/rakshakanthraj/chicago-taxi-data-pipeline.git
cd chicago-taxi-data-pipeline
```

Run snapshots:

```bash
dbt snapshot
```

Build Gold models:

```bash
dbt run
```

---

## What I Learned

Through this project I gained hands-on experience in:

* Designing Medallion Architecture pipelines
* Building ETL pipelines using PySpark
* Delta Lake processing
* Implementing SCD Type 2
* Point-in-Time joins
* Star schema modeling
* Revenue reconciliation
* Data quality validation
* dbt model development

---

## Future Improvements

* Orchestrate the pipeline using Databricks Workflows
* Add dbt tests
* Implement CI/CD using GitHub Actions
* Build Power BI dashboards
* Optimize incremental processing

---

## Author

**Raksha GK**

GitHub: https://github.com/rakshakanthraj
