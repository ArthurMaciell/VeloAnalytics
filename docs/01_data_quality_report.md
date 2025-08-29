# VeloNorth - Data Quality Assessment Report

This document outlines the data quality issues identified during the initial exploration of the raw CSV datasets and details the automated solutions implemented within the **DataTransformation** component of the VeloAnalytics pipeline to address them.

---

## 1. Duplicate Keys

**Assessment:**  
- Analysis of the raw data revealed potential duplicate records in tables that should have unique primary keys (e.g., multiple entries for the same `PRODUCTID` in `Products.csv`).  
- This poses a significant risk to data integrity, potentially leading to incorrect aggregations and skewed metrics.  

**Automated Solution:**  
- A `PRIMARY_KEYS` section was added to the `schema.yaml` file, formally defining the unique identifier(s) for each critical table.  
- The DataTransformation component reads this schema and programmatically applies a `drop_duplicates()` operation based on the defined primary key for each table.  

**Outcome:**  
- Guarantees that the processed data in `data/02_processed` is free from duplicate primary key entries.  
- Ensures the reliability of the final data model.  

---

## 2. Inconsistent & Ambiguous Data

**Assessment:**  
Several inconsistencies were identified across the dataset:  
- **Corrupted Column Headers:** `Addresses.csv` contained a hidden Byte Order Mark (BOM), causing the first column to be read as `"ï»¿ADDRESSID"` instead of `"ADDRESSID"`.  
- **Empty String Values:** Columns such as `NOTEID` contained empty spaces (`' '`) instead of true nulls, making them harder to detect.  
- **Implicit Date Formats:** Date columns were stored as integers (e.g., `20181003`), requiring consistent conversion logic.  

**Automated Solution:**  
- **Column Name Cleaning:** Automatic cleaning of all column headers upon file load, removing BOMs and whitespace.  
- **Standardization of Nulls:** Regex replacement (`r'^\s*$'`) converts empty/whitespace-only strings to `pd.NA`, standardizing missing values.  
- **Date Conversion Logic:** A rule detects columns ending in `"at"` or `"date"` and converts them to `datetime` objects using the `'%Y%m%d'` format.  

---

## 3. Missing Data

**Assessment:**  
- Some columns, especially in `Products` (e.g., `WIDTH`, `DEPTH`, `HEIGHT`) and `BusinessPartners` (`CREATEDBY`), were found to be entirely null.  

**Automated Solution:**  
- **Strategic Imputation:**  
  - Missing numeric values → filled with `0`.  
  - Missing text (object) values → filled with `"N/A"`.  

**Outcome:**  
- Prevents errors in downstream calculations.  
- Makes missing data explicit and consistent in final reports, rather than leaving blanks.  

---

## 4. Referential Integrity

**Assessment:**  
- A full referential integrity check (e.g., ensuring every `PRODUCTID` in `SalesOrderItems` exists in `Products`) was **not implemented** in this version to maintain scope and performance.  
- In production, missing references could lead to **orphaned fact records**.  

**Recommendation (Future Work):**  
- Add a dedicated data validation step performing **LEFT JOIN checks** between fact and dimension tables.  
- Any records failing the integrity check should be logged into an **exceptions table** for manual review.  
- This prevents corrupted or incomplete records from propagating into the analytical model.  

---
