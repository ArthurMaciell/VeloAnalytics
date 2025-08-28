import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(
    page_title="Bike Sales BI Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading ---
# This function will cache the data to improve performance
@st.cache_data
def load_data(presentation_path: Path) -> dict:
    """
    Loads all presentation Parquet files into a dictionary of pandas DataFrames.
    """
    dataframes = {}
    for file_name in os.listdir(presentation_path):
        if file_name.endswith('.parquet'):
            table_name = Path(file_name).stem
            dataframes[table_name] = pd.read_parquet(os.path.join(presentation_path, file_name))
    return dataframes

# --- Main Application ---
def main():
    st.title("🚲 Bike Sales BI & Data Modelling Dashboard")
    
    # Define the path to the presentation data
    presentation_path = Path("data/03_presentation")
    
    # Load the data
    try:
        data_frames = load_data(presentation_path)
        fact_sales = data_frames.get('fact_sales')
        
        if fact_sales is not None:
            st.success("Data loaded successfully!")
            st.dataframe(fact_sales.head())
        else:
            st.error("Could not load the fact_sales table. Please run the data pipeline.")

    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        st.info("Please ensure the data pipeline has been run successfully by executing 'python main.py'")


if __name__ == "__main__":
    main()