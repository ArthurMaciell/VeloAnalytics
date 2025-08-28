# 3. Metrics & Calculations

This document specifies the calculation logic for key business metrics derived from the analytical data model.  
The logic is presented in pseudo-code, which can be easily translated into **SQL**, **DAX**, or **Python**.

---

## 1. Total Revenue
Measures the total gross sales amount across all transactions.  
This is the primary indicator of sales performance.

**Calculation Logic (Pseudo-code):**

---

## 2. Average Order Value (AOV)
Indicates the average gross amount spent per unique sales order.  
This metric helps understand customer purchasing behavior.

**Calculation Logic (Pseudo-code):**


---

## 3. Total Quantity Sold
Measures the total number of individual items sold.  
This is a key indicator of product volume and operational scale.

**Calculation Logic (Pseudo-code):**
```bash
Total Revenue = SUM(fact_sales[GROSSAMOUNT])
```

---

## 4. Top 5 Products by Revenue
Identifies the products that contribute the most to the total revenue, allowing for a focus on high-value items.

**Calculation Logic (Pseudo-code):**


---

## 5. Order Conversion Rate by Status
Measures the percentage of orders that are completed versus those that are blocked or delayed.  
This is a key metric for operational efficiency.

**Calculation Logic (Pseudo-code):**

Total Orders = COUNT_DISTINCT(fact_sales[SALESORDERID])
Completed Orders = COUNT_DISTINCT(fact_sales[SALESORDERID] WHERE fact_sales[LifecycleStatus] = 'C')
Conversion Rate = (Completed Orders / Total Orders) * 100