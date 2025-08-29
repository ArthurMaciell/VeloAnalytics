# VeloNorth - Data Model Enrichment Proposals

This document outlines four strategic proposals to enrich the existing analytical data model.  
These enhancements will enable deeper business insights by integrating external data and creating valuable derived features, directly addressing the **advanced tasks** section of the technical challenge.

---

## Proposal 1: Geographic & Demographic Enrichment (External Data)

**Objective:**  
Understand the market characteristics of different sales regions beyond just the country name.

**Method:**  
- Enrich **`dim_customer`**: Use the `COUNTRY` and `CITY` columns to join with external demographic and economic datasets.

**External Data Sources:**  
- **World Bank Open Data**: Country-level GDP per capita, population, and internet penetration.  
- **Public City-Level Datasets**: CSVs from Numbeo or national statistics offices with city-level population/economic indicators.

**New Analytical Capabilities:**  
- *Market Penetration Analysis*: Correlate sales volume with population to estimate market share.  
- *Economic Correlation*: Analyze relationships between GDP per capita and average bike prices.  
- *Strategic Planning*: Identify underserved but high-potential regions for targeted marketing campaigns.  

---

## Proposal 2: Product Feature Engineering (Derived Data)

**Objective:**  
Analyze product performance based on intrinsic characteristics, not just categories.

**Method:**  
- Enrich **`dim_product`**: Add new derived attributes based on existing fields.

**Derived Features to Create:**  
- **Price Tier**: Categorize products into `Low`, `Medium`, `High`, `Premium` using the `PRICE` column.  
  - Example: `< $1000 = Low`, `$1000–$2500 = Medium`, `$2500–$5000 = High`, `> $5000 = Premium`.  
- **Weight Class**: Categorize products as `Lightweight`, `Standard`, or `Heavyweight` using `WEIGHTMEASURE`.

**New Analytical Capabilities:**  
- *Price Point Analysis*: Identify which tiers drive the most revenue and margins.  
- *Product Segmentation*: Explore correlations between weight, price, and sales volume. Useful for product design and inventory management.  

---

## Proposal 3: Advanced Time-Based Analysis (Derived Data)

**Objective:**  
Uncover deeper sales patterns and customer behaviors by enhancing time-based analysis.

**Method:**  
- Enrich **`dim_date`**: Add richer time-based features.

**Derived Features to Create:**  
- **Is_Weekend**: Boolean (True/False) to compare weekday vs weekend sales.  
- **Season**: Map month → `Spring`, `Summer`, `Autumn`, `Winter`.  
- **Holiday Indicator**: Boolean (True/False), requires external holiday datasets for major countries (Canada, US, Germany).

**New Analytical Capabilities:**  
- *Behavioral Patterns*: Detect if premium bikes sell more on weekends or if certain models peak in summer.  
- *Campaign Effectiveness*: Measure lift during holidays and evaluate marketing ROI.  
- *Operational Planning*: Improve forecasting and inventory planning with seasonal demand patterns.  

---

## Proposal 4: Simple Sales Forecasting (Predictive Model)

**Objective:**  
Develop a simple predictive model to forecast monthly sales revenue.

**Method:**  
1. **Data Preparation:** Aggregate `fact_sales` into monthly net revenue time series.  
2. **Feature Engineering:**  
   - Extract `month`, `year`, `quarter`.  
   - Add **Lag features** (t-1, t-3).  
   - Add **Rolling Averages** (3-month, 6-month).  
3. **Model Selection:**  
   - Start with **Linear Regression**.  
   - Optionally test a boosting model (e.g., **LightGBM**).  
4. **Training & Evaluation:**  
   - Train/test split on historical data.  
   - Evaluate with **MAE (Mean Absolute Error)**.

**New Analytical Capabilities:**  
- *Proactive Inventory Management*: Anticipate demand and optimize stock levels.  
- *Financial Planning*: Support budgeting with data-driven projections.  
- *Target Setting*: Define realistic sales targets backed by predictive analysis.  

---
