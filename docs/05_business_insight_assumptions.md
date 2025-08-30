# VeloNorth - Business Insights & Key Assumptions

This document explains the key business insights that the **VeloNorth Analytics Dashboard** is designed to deliver.  
It also outlines the key assumptions made during the data modelling and analysis process.

---

## Business Insights Delivered by the Dashboard

The dashboard is designed to move beyond raw data and provide **actionable insights** for key business areas, including sales strategy, product management, and operational efficiency.

---

### Overall Business Performance at a Glance
- **Insight:** Provides an immediate, high-level understanding of the company's health.  
- **How:** KPI cards (`Total Net Revenue`, `Total Completed Orders`, `Average Order Value`) offer a real-time snapshot of performance, allowing leadership to quickly assess if the business is on track.

---

### Sales Seasonality and Growth Trends
- **Insight:** Identifies patterns in sales over time, such as peak months or periods of growth/decline.  
- **How:** The **Sales Trend Over Time** line chart visualizes monthly revenue, making it easy to spot seasonality. This supports marketing planning and inventory management for high-demand periods.

---

### Top-Performing Products and Categories
- **Insight:** Pinpoints which products and categories are the main drivers of revenue.  
- **How:** The **Revenue by Product Category** bar chart ranks categories by sales. This enables the business to focus marketing, manage stock for popular items, and identify underperforming product lines.

---

### Key Geographic Markets
- **Insight:** Identifies the most profitable countries and regions.  
- **How:** Interactive filters and charts allow users to drill down into geographic areas. This helps prioritize sales efforts in high-performing regions and uncover potential markets for expansion.

---

### High-Value Customer Identification
- **Insight:** Determines which customers are most valuable to the business.  
- **How:** The **Top 10 Customers by Revenue** table provides an instant list of key accounts. This enables sales teams to design loyalty programs and targeted retention strategies.

---

### Sales Channel Effectiveness
- **Insight:** Compares the performance of different sales channels (e.g., direct customers vs. resellers).  
- **How:** The **Revenue by Sales Channel** chart breaks down revenue by `PARTNERROLE`, helping leadership identify the most effective channels and optimize sales strategy accordingly.

---

## Key Assumptions

The analysis and the data model were built upon the following assumptions:

1. **Source of Truth for Financials:**  
   - The `SalesOrderItems` (line item) table is the **single source of truth** for financial calculations.  
   - Pre-aggregated totals in the `SalesOrders` (header) table were considered unreliable and intentionally excluded from revenue metrics.

2. **Definition of a Completed Sale:**  
   - KPIs and financial charts are based on the assumption that `LIFECYCLESTATUS = 'C'` indicates a fully completed and recognized sale.

3. **Sales Channel Interpretation:**  
   - The `PARTNERROLE` column in `BusinessPartners` represents the sales channel:  
     - `1` = **Reseller**  
     - `2` = **Direct Customer**

4. **Data Completeness:**  
   - The nine provided CSV files are assumed to represent a complete and accurate snapshot of business operations for the given time period.

---
