# 3. Metrics & Calculations

This document specifies the calculation logic for key business metrics derived from the analytical data model.  
The logic is presented in pseudo-code, which can be easily translated into **SQL**, **DAX**, or **Python**.

---

## 1. Total Revenue
Measures the total gross sales amount across all transactions.  
This is the primary indicator of sales performance.

**Calculation Logic (Pseudo-code):**
``` bash
Total Revenue = SUM(fact_sales[GROSSAMOUNT])
```

---

## 2. Average Order Value (AOV)
Indicates the average gross amount spent per unique sales order.  
This metric helps understand customer purchasing behavior.

**Calculation Logic (Pseudo-code):**
``` bash
Total Revenue = SUM(fact_sales[GROSSAMOUNT])
Unique Orders = COUNT_DISTINCT(fact_sales[SALESORDERID])
Average Order Value = Total Revenue / Unique Orders

```

---

## 3. Total Quantity Sold
Measures the total number of individual items sold.  
This is a key indicator of product volume and operational scale.

**Calculation Logic (Pseudo-code):**
``` bash
Total Quantity Sold = SUM(fact_sales[QUANTITY])
```

---

## 4. Top 5 Products by Revenue
Identifies the products that contribute the most to the total revenue, allowing for a focus on high-value items.

**Calculation Logic (Pseudo-code):**
``` bash
1. JOIN fact_sales ON dim_product using PRODUCTID
2. GROUP BY dim_product[Product Name]
3. CALCULATE Revenue = SUM(fact_sales[GROSSAMOUNT]) for each group
4. ORDER results by Revenue in descending order
5. SELECT TOP 5
```

---

## 5. Order Conversion Rate by Status
Measures the percentage of orders that are completed versus those that are blocked or delayed.  
This is a key metric for operational efficiency.

**Calculation Logic (Pseudo-code):**

``` bash
Total Orders = COUNT_DISTINCT(fact_sales[SALESORDERID])
Completed Orders = COUNT_DISTINCT(fact_sales[SALESORDERID] WHERE fact_sales[LifecycleStatus] = 'C')
Conversion Rate = (Completed Orders / Total Orders) * 100
```