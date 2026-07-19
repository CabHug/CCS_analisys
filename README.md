# CCS Business Data infraestructure modernization

> End-to-end Data Engineering pipeline designed to automate the generation of a centralized business database for **CCS**, transforming raw Excel source files into structured, analytics-ready datasets for Power BI reporting.

---

## 📌 Project Overview

This project is a critical component of the **Data-Driven transition at CCS**. It streamlines the transformation of raw business data—stored in a multi-year, monthly folder structure—into a robust, consolidated database.

The pipeline automates the ingestion, cleaning, and normalization of financial and sales data. It eliminates manual intervention by providing an interactive interface that processes records, standardizes inconsistent naming conventions, fills missing values, and generates the final CSV outputs required for high-level business intelligence in Power BI.

---

## 🎯 Objectives

- **Automate ETL Processes:** Replace manual data handling with a structured, reproducible pipeline.
- **Data Normalization:** Clean and unify inconsistent naming conventions across business records.
- **Business Logic Integration:** Implement logic to handle missing data through intelligent record inference.
- **Interactive Workflow:** Provide a user-friendly CLI menu for seamless orchestration.
- **BI Readiness:** Generate optimized, clean CSV tables ready for immediate consumption in Power BI.

---

## 🏗️ Pipeline Architecture

The pipeline is designed with a modular approach, separating extraction, transformation, and load (ETL) logic from the user interface.

```text
          Raw Sources (.xlsm)
                  │
                  ▼
        ┌───────────────────┐
        │      ETL.py       │ ◄─── Data Cleaning, Normalization
        │ (Raw Processing)  │      & Missing Data Imputation
        └───────────────────┘
                  │
                  ▼
        ┌───────────────────┐
        │   Table_ETL.py    │ ◄─── Database Schema Update
        │ (Table Creation)  │      (11 Core Business Tables)
        └───────────────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ transform_to_csv  │ ◄─── BI Data Preparation
        │  (Export Layer)   │      (Power BI Ready)
        └───────────────────┘
```
---
## 📂 Project Structure
Plaintext
```text
ccs-business-analytics/
├── data_source/
│   ├── 2024/
│   ├── 2025/
│   ├── 2026/         
│   ├── cleaned/      
│   └── rejected/       
├── DB_tables/
│   ├── a_base            
│   └── a_csv_tables
├── Power_BI_analysis/
│   └── CCS_reporte_2026.pbix
├── menu.py             
├── README.md
├── config.json
├── ETL.py
├── OOP_classes.py
├── normalize_map.py
├── table_ETL.py
├── transform_tocsv.py
└── update_db.py
```

---
## ⚙️ Core Modules

### 1. Data Ingestion & Cleaning (ETL.py)
Reads raw files (CCS_YYYY_Month.xlsm).

Performs data imputation by taking data from similar records.

Normalizes records to handle synonymous names.

Output: Structured files for each processed source.

### 2. Database Management (Table_ETL.py)
Maintains a centralized record repository.

Manages 11 core tables:
ciudad_region, clientes, curso, descuento, genero, medio_de_pago, modalidad, procedencia, profesion, responsable_ventas, ventas.

Ensures the information is updated with new records in every execution.

### 3. BI Export Layer (transform_to_csv.py)
Converts processed database tables into clean CSV format.

Optimized for direct ingestion into Power BI reports.

---
## 🚀 How to Run
The project features an interactive menu to orchestrate the process. Simply run:

Bash
python menu.py
Workflow Pipeline:

Read raw data (ETL): Extracts and cleans new source files.

Table creation (ETL): Updates the core business database with new records.

Convert to CSV: Generates final files for Power BI.

---
## 💡 Key Features
Standardization: Resolves naming inconsistencies automatically across different monthly sources.

Scalability: Handles multi-year historical folder structures.

Maintainability: Modular code allows for easy updates to specific business rules.

User-Centric: Designed for non-technical users via the menu.py interface.

---
## 📬 Contact
Hugo Cabrera

LinkedIn: https://www.linkedin.com/in/hugo-cabrera-324272191/

GitHub: https://github.com/CabHug

Note: This project is part of the digital transformation initiative at CCS, aimed at ensuring high-quality, reliable data for strategic decision-making.