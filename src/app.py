import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

# --- PAGE CONFIGURATION ---
# This must be the first Streamlit command in your script.
st.set_page_config(
    page_title="VeloNorth Analytics Dashboard",
    page_icon=":bike:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PATHS ---
# Define the path to the presentation data directory.
PRESENTATION_DIR = Path(__file__).resolve().parent.parent / "data" / "03_presentation"

# --- DATA LOADING ---
# A professional practice is to cache the data loading to improve performance.
@st.cache_data
def load_data():
    """
    Loads all necessary parquet files from the presentation layer.
    Returns a dictionary of dataframes.
    """
    data_files = {
        "fact_sales": "fact_sales.parquet",
        "dim_customer": "dim_customer.parquet",
        "dim_product": "dim_product.parquet",
        "dim_employee": "dim_employee.parquet",
        "dim_date": "dim_date.parquet"
    }
    df_dict = {}
    for key, file_name in data_files.items():
        file_path = os.path.join(PRESENTATION_DIR, file_name)
        if os.path.exists(file_path):
            df_dict[key] = pd.read_parquet(file_path)
        else:
            st.error(f"Data file not found: {file_name}")
            return None
            
    # Convert date columns to datetime objects for proper filtering and plotting
    df_dict['fact_sales']['OrderDate'] = pd.to_datetime(df_dict['fact_sales']['OrderDate'])
    df_dict['dim_date']['Date'] = pd.to_datetime(df_dict['dim_date']['Date'])
    
    return df_dict

dataframes = load_data()

if dataframes:
    fact_sales = dataframes["fact_sales"]
    dim_customer = dataframes["dim_customer"]
    dim_product = dataframes["dim_product"]
    dim_employee = dataframes["dim_employee"]
    dim_date = dataframes["dim_date"]

    # --- SIDEBAR ---
    # The sidebar is used for filters.
    st.sidebar.image("logo.png", width=150) # Make sure you have a logo.png file
    st.sidebar.title("Dashboard Filters")

    # Date Range Filter
    min_date = dim_date['Date'].min().date()
    max_date = dim_date['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Country Filter (Multiselect)
    all_countries = sorted(dim_customer['COUNTRY'].unique())
    selected_countries = st.sidebar.multiselect(
        "Select Country",
        options=all_countries,
        default=all_countries
    )

    # Product Category Filter
    all_categories = sorted(dim_product['SHORT_DESCR_y'].unique())
    selected_categories = st.sidebar.multiselect(
        "Select Product Category",
        options=all_categories,
        default=all_categories
    )

    # --- FILTERING DATA ---
    # Apply filters to the fact table based on user selections.
    start_date, end_date = date_range
    
    filtered_sales = fact_sales[
        (fact_sales['OrderDate'].dt.date >= start_date) &
        (fact_sales['OrderDate'].dt.date <= end_date)
    ]
    
    # Merge with dimensions to get filterable columns
    filtered_sales = pd.merge(filtered_sales, dim_customer[['PARTNERID', 'COUNTRY']], on='PARTNERID', how='left')
    filtered_sales = pd.merge(filtered_sales, dim_product[['PRODUCTID', 'SHORT_DESCR_y']], on='PRODUCTID', how='left')
    
    if selected_countries:
        filtered_sales = filtered_sales[filtered_sales['COUNTRY'].isin(selected_countries)]
    
    if selected_categories:
        filtered_sales = filtered_sales[filtered_sales['SHORT_DESCR_y'].isin(selected_categories)]

    # --- MAIN PAGE ---
    st.title(" VeloNorth Sales Analytics Dashboard")
    st.markdown("---")

    # --- KPIs ---
    total_revenue = filtered_sales['GROSSAMOUNT'].sum()
    total_orders = filtered_sales['SALESORDERID'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    total_quantity = filtered_sales['QUANTITY'].sum()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    kpi2.metric(label="Total Orders", value=f"{total_orders:,}")
    kpi3.metric(label="Avg. Order Value", value=f"${avg_order_value:,.2f}")
    kpi4.metric(label="Total Quantity Sold", value=f"{total_quantity:,}")
    
    st.markdown("---")

    # --- CHARTS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Product Category")
        revenue_by_category = filtered_sales.groupby('SHORT_DESCR_y')['GROSSAMOUNT'].sum().sort_values(ascending=False).reset_index()
        fig_cat = px.bar(
            revenue_by_category,
            x='GROSSAMOUNT',
            y='SHORT_DESCR_y',
            orientation='h',
            title='Top Product Categories by Revenue',
            labels={'GROSSAMOUNT': 'Total Revenue ($)', 'SHORT_DESCR_y': 'Product Category'},
            template='plotly_white'
        )
        fig_cat.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        st.subheader("Revenue by Country")
        revenue_by_country = filtered_sales.groupby('COUNTRY')['GROSSAMOUNT'].sum().sort_values(ascending=False).reset_index()
        fig_country = px.pie(
            revenue_by_country,
            values='GROSSAMOUNT',
            names='COUNTRY',
            title='Revenue Distribution by Country',
            hole=.3,
            template='plotly_white'
        )
        st.plotly_chart(fig_country, use_container_width=True)

    st.markdown("### Sales Trend Over Time")
    # Resample data for time series analysis
    sales_over_time = filtered_sales.set_index('OrderDate').resample('M')['GROSSAMOUNT'].sum().reset_index()
    fig_time = px.line(
        sales_over_time,
        x='OrderDate',
        y='GROSSAMOUNT',
        title='Monthly Sales Revenue',
        labels={'GROSSAMOUNT': 'Total Revenue ($)', 'OrderDate': 'Month'},
        template='plotly_white'
    )
    st.plotly_chart(fig_time, use_container_width=True)

    # --- DATA TABLE ---
    st.markdown("### Detailed Sales Data")
    # Show a sample of the detailed, filtered data
    st.dataframe(filtered_sales.head(100))

else:
    st.warning("Data could not be loaded. Please ensure the data pipeline has been run successfully.")


