# VeloNorth - Data Model Enrichment Proposals

This document outlines three strategic proposals to enrich the existing analytical data model.  
These enhancements will enable deeper business insights by integrating external data and creating valuable derived features, directly addressing the **advanced tasks** section of the technical challenge.

---

## Proposal 1: Geographic & Demographic Enrichment (External Data)

**Objective:**  
To understand the market characteristics of different sales regions beyond just the country name.

**Method:**  
- Enrich **`dim_customer`**: Use the `COUNTRY` and `CITY` information from the `dim_customer` table to join with external demographic and economic datasets.

**External Data Sources:**  
- **World Bank Open Data**: Public API providing country-level data such as GDP per capita, population, and internet penetration.  
- **Public City-Level Datasets**: Static CSV files from sources like Numbeo or national statistics offices for city-level indicators.

**New Analytical Capabilities:**  
- *Market Penetration Analysis*: Correlate sales volume with regional population to estimate market share.  
- *Economic Correlation*: Analyze if there is a relationship between a country’s GDP per capita and the average bike price.  
- *Strategic Planning*: Identify underserved but high-potential regions for future marketing campaigns.  

---

## Proposal 2: Product Feature Engineering (Derived Data)

**Objective:**  
To analyze product performance based on intrinsic characteristics, not just categories.

**Method:**  
- Enrich **`dim_product`**: Create new, derived columns within the `dim_product` table based on existing data.

**Derived Features to Create:**  
- **Price Tier**: Create categories (`Low`, `Medium`, `High`, `Premium`) using brackets on the `PRICE` column.  
  - Example: `< $1000 = Low`, `$1000–$2500 = Medium`, etc.  
- **Weight Class**: Categorize as `Lightweight`, `Standard`, or `Heavyweight` using the `WEIGHTMEASURE` column.  

**New Analytical Capabilities:**  
- *Price Point Analysis*: Answer questions like “Which price tier generates the most revenue?” or “Are premium bikes selling better in specific regions?”  
- *Product Segmentation*: Explore correlations between weight, price, and sales volume → insights for product development and inventory management.  

---

## Proposal 3: Advanced Time-Based Analysis (Derived Data)

**Objective:**  
To uncover deeper sales patterns and customer behaviors by enhancing our time-based analysis.

**Method:**  
- Enrich **`dim_date`**: Add more sophisticated attributes to the date dimension.

**Derived Features to Create:**  
- **Is_Weekend**: Boolean (`True/False`) to compare weekday vs weekend sales.  
- **Season**: Categorize months into `Spring`, `Summer`, `Autumn`, `Winter`.  
- **Public Holiday Indicator**: Boolean (`True/False`), requires external datasets of holidays for key countries (Canada, US, Germany, etc.).  

**New Analytical Capabilities:**  
- *Behavioral Pattern Recognition*: Check if customers buy more expensive bikes on weekends or if certain categories peak in specific seasons.  
- *Campaign Effectiveness*: Measure sales lift during holiday periods to evaluate marketing campaign success.  
- *Operational Planning*: Use seasonality insights to improve demand forecasting and inventory management.  

---
