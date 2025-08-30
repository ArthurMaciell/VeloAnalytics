# VeloNorth - Sales Analytics & BI Pipeline

This repository contains the end-to-end solution for the **"Bikes Sales BI & Data Modelling Challenge"**.  
The project features a robust, automated data pipeline built with Python and a final interactive analytics dashboard developed with **Streamlit**.

---

## 🚀 Project Overview
The primary goal of this project is to transform a raw dataset of nine CSV files into a clean, robust analytical data model and use it to deliver **key business insights**.  

The solution follows professional **software engineering** and **data engineering** best practices, including modular code, configuration management, and automated data processing.

### Key Features
- **Automated Data Pipeline**: Multi-stage pipeline (Ingestion, Validation, Transformation, Modelling) that processes raw data into an analysis-ready format.  
- **Robust Data Modelling**: Implements a **Star Schema** with a central fact table and multiple dimension tables, optimized for BI reporting.  
- **Comprehensive Data Quality Checks**: Automatically handles common data quality issues like duplicate keys, inconsistent values, and schema mismatches.  
- **Interactive Analytics Dashboard**: Built with **Streamlit**, offering dynamic filtering, currency conversion, and answers to key business questions.  
- **Professional Documentation**: Includes detailed reports on data quality, model schema, and business insights.  

---

## 🛠️ Tech Stack
- **Language**: Python 3.9+  
- **Data Processing**: pandas  
- **Dashboard**: Streamlit 
- **Prototyping**: Power BI  
- **Core Libraries**: python-box, ensure, nbformat, requests, zipfile

---

## 📂 Project Structure
The project follows a **modular and scalable structure** to separate concerns:

```
├── data/              # Stores data assets (raw, processed, presentation)
├── docs/              # Documentation (Data Quality, Model Schema, etc.)
├── notebooks/         # Jupyter notebooks for exploratory data analysis (EDA)
├── src/               # Main source code for the application
│   ├── components/    # Components for each pipeline stage
│   ├── config/        # Configuration management
│   ├── entity/        # Configuration data structures
│   ├── pipeline/      # Orchestration scripts
│   ├── logger_config/ # Custom logging configuration
│   └── utils.py       # Utility functions
├── app.py             # Streamlit dashboard entry point
├── main.py            # Runs the entire data pipeline
├── config.yaml        # Main configuration file
├── schema.yaml        # Data schema definitions
├── setup.py           # Makes the project installable as a package
└── requirements.txt   # Python dependencies
```

---

## ⚙️ Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ArthurMaciell/VeloAnalytics.git
cd VeloAnalytics
```

### 2. Create and Activate a Virtual Environment
```bash
# Create the environment
python -m venv .venv

# Activate the environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install the Project as a Local Package
This makes the custom modules importable:
```bash
pip install -e .
```

---

## ▶️ How to Run

### 1. Run the Data Pipeline
Processes raw CSVs into the final analytical model:
```bash
python main.py
```
This executes **Ingestion → Validation → Transformation → Modelling** and outputs the final data to `data/03_presentation/`.

### 2. Launch the Interactive Dashboard
```bash
streamlit run src/app.py
```
Opens the **Streamlit dashboard** in your default web browser.

---

## 📚 Project Documentation
This repository includes detailed documentation covering the key aspects of the challenge:

- **Data Quality Assessment Report** → Issues identified & automated fixes.  
- **Analytical Data Model Schema** → Star Schema sketch with keys & relationships.  
- **Business Metrics Definitions** → Logic for KPIs (Revenue, AOV, Conversion, etc.).  
- **Model Enrichment Proposals** → External data integration & predictive forecasting.  
- **Business Insights & Assumptions** → Key insights delivered by the dashboard.  

---
