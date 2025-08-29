# VeloNorth - Analytical Data Model Schema

This document provides a schema sketch of the analytical data model designed for the **VeloNorth** project.  
The model is structured as a **Star Schema**, which is optimized for fast and efficient BI reporting and analysis.

---

## Schema Overview
- **Fact Table**: `fact_sales` — contains quantitative measures of business events.  
- **Dimension Tables**:  
  - `dim_product`  
  - `dim_customer`  
  - `dim_employee`  
  - `dim_date`  

**Cardinality:**  
All relationships are **one-to-many (1–*)**, flowing from the dimension tables to the fact table.

---

## Entity-Relationship Diagram (Sketch)


+-----------------+      +-----------------+      +-----------------+
|   dim_date      |      |  dim_employee   |      |  dim_customer   |
|-----------------|      |-----------------|      |-----------------|
| PK | Date       | 1--* | PK | EMPLOYEEID | 1--* | PK | PARTNERID  |
|    | Year       |      |    | NAME_FIRST |      |    | COMPANYNAME|
|    | Month      |      |    | NAME_LAST  |      |    | COUNTRY    |
|    | Quarter    |      |    |EMAILADDRESS|      |    | CITY       |
|    | DayOfWeek  |      |    | ...        |      |    | ...        |
+-----------------+      +-----------------+      +-----------------+
        |                      |                      |
        |                      |                      |
+-------------------------------------------------------------------+
|                            fact_sales                             |
|-------------------------------------------------------------------|
| FK | OrderDate                                                    |
| FK | EMPLOYEEID                                                   |
| FK | PARTNERID                                                    |
| FK | PRODUCTID                                                    |
|    | GROSSAMOUNT (Measure)                                        |
|    | NETAMOUNT (Measure)                                          |
|    | QUANTITY (Measure)                                           |
|    | LIFECYCLESTATUS                                              |
|    | ...                                                          |
+-------------------------------------------------------------------+
                               |
                               |
                      +-----------------+
                      |   dim_product   |
                      |-----------------|
                      | PK | PRODUCTID  |
                      |    | SHORT_DESCR|
                      |    | CATEGORY   |
                      |    | PRICE      |
                      |    | ...        |
                      +-----------------+


## Table Definitions

### fact_sales
- **Grain:** One row per product line item on a sales order.  
- **Description:** Contains detailed measures for each sales transaction.  
- **Keys:**  
  - `OrderDate` → FK to `dim_date.Date`  
  - `EMPLOYEEID` → FK to `dim_employee.EMPLOYEEID`  
  - `PARTNERID` → FK to `dim_customer.PARTNERID`  
  - `PRODUCTID` → FK to `dim_product.PRODUCTID`  

---

### dim_product
- **Grain:** One row per unique product.  
- **Description:** Contains descriptive attributes of each product.  
- **Primary Key:** `PRODUCTID`  

---

### dim_customer
- **Grain:** One row per unique customer.  
- **Description:** Contains descriptive attributes of each customer.  
- **Primary Key:** `PARTNERID`  

---

### dim_employee
- **Grain:** One row per unique employee.  
- **Description:** Contains descriptive attributes of each employee.  
- **Primary Key:** `EMPLOYEEID`  

---

### dim_date
- **Grain:** One row per day.  
- **Description:** A generated calendar table for robust time-based analysis.  
- **Primary Key:** `Date`  