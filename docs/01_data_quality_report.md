# VeloNorth - Data Quality Assessment Report

This document outlines the data quality issues identified during the initial exploration of the raw CSV datasets and details the automated solutions implemented within the **DataTransformation** component of the VeloAnalytics pipeline to address them.

---

## 1. Duplicate Keys & Data Redundancy

**Assessment:**  
- In `ProductTexts.csv`, some products contain descriptions in multiple languages (e.g., English `EN` and German `DE`).  
- While not strictly a duplicate key issue, this redundancy had to be handled to ensure a clean model where each product appears only once.  
- In `SalesOrderItems`, the `SALESORDERID` is intentionally repeated for multiple items in the same order. To ensure uniqueness, a **composite key** (`SALESORDERID`, `SALESORDERITEM`) is required.  
- Best practices for robust pipelines require handling composite keys and validating uniqueness to prevent future data entry issues.  

**Automated Solution:**  
- A `PRIMARY_KEYS` section was added to `schema.yaml`, formally defining unique identifiers for each table.  
- For multi-language tables, composite keys (e.g., `[PRODUCTID, LANGUAGE]`) were defined.  
- The DataTransformation component applies `drop_duplicates()` based on these keys.  
- In the DataModelling stage, an explicit filter (`LANGUAGE == 'EN'`) ensures single-language joins from `ProductTexts`.  

**Outcome:**  
- Final dimension tables are clean, consistent (single language), and free from duplicates, ensuring data integrity.  

---

## 2. Mismatched Financial Aggregations

**Assessment:**  
- Aggregated financial columns (`GROSSAMOUNT`, `NETAMOUNT`, `TAXAMOUNT`) in `SalesOrders` (header) **do not match** the sum of values in `SalesOrderItems` (line items) for the same `SALESORDERID`.  

**Hypothesis:**  
- Header-level totals likely include **extra charges** (e.g., shipping, handling) not itemized in line items.  

**Automated Solution:**  
- Architectural decision: use the **most granular data** (`SalesOrderItems`) as the single source of truth.  
- The `fact_sales` table was designed with grain = **one row per sales order item**.  

**Outcome:**  
- All financial metrics (e.g., Revenue) are calculated bottom-up from line items.  
- Header-level pre-aggregates are ignored, ensuring product sales reporting is accurate and reproducible.  

---

## 3. Inconsistent & Ambiguous Data

**Assessment:**  
Identified inconsistencies included:  
- **Corrupted Column Headers:** `Addresses.csv` contained a BOM, making the first column `"ï»¿ADDRESSID"`.  
- **Empty String Values:** Columns like `NOTEID` had blank spaces instead of nulls.  
- **Implicit Date Formats:** Dates were stored as integers (`20181003`) requiring consistent conversion.  

**Automated Solution:**  
- **Column Name Cleaning:** Automatically strip BOMs and whitespace from headers.  
- **Standardization of Nulls:** Regex (`r'^\s*$'`) replaces empty/whitespace with `pd.NA`.  
- **Date Conversion Logic:** Automatically detect columns ending in `"at"` or `"date"` and convert to `datetime` with `'%Y%m%d'` format.  

---

## 4. Missing Data

**Assessment:**  
- Some columns were entirely null (e.g., `WIDTH`, `DEPTH`, `HEIGHT` in Products; `CREATEDBY` in BusinessPartners).  

**Automated Solution:**  
- **Strategic Imputation:**  
  - Numeric columns → filled with `0`.  
  - Text columns → filled with `"N/A"`.  

**Outcome:**  
- Prevents errors in downstream analysis.  
- Makes missing values explicit and consistent in final reports.  

---

## 5. Referential Integrity

**Assessment:**  
- No full referential integrity check implemented (e.g., validating every `PRODUCTID` in `SalesOrderItems` exists in `Products`).  
- Without it, there is risk of **orphaned fact records**.  

**Recommendation (Future Work):**  
- Add a dedicated validation step:  
  - Perform **LEFT JOIN checks** between fact and dimension tables.  
  - Log missing references in an **exceptions table** for manual review.  
- This ensures corrupted or incomplete records do not enter the analytical model.  

---
