import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path
import requests # Import the new library

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="VeloNorth Analytics Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PATHS ---
PRESENTATION_DIR = Path(__file__).resolve().parent.parent / "data" / "03_presentation"

# --- CURRENCY SYMBOLS ---
# A dictionary to map currency codes to their symbols for professional formatting
currency_symbols = {
    "USD": "$", "CAD": "C$", "EUR": "€", "BRL": "R$", "JPY": "¥",
    "GBP": "£", "AUD": "A$", "CNY": "¥", "INR": "₹"
}


# --- API & DATA LOADING ---
@st.cache_data(ttl=3600) # Cache the data for 1 hour
def get_exchange_rates(base_currency="USD"):
    """Fetches latest exchange rates from a free API."""
    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base_currency}")
        response.raise_for_status()
        return response.json()["rates"]
    except requests.exceptions.RequestException as e:
        st.error(f"Could not fetch exchange rates: {e}")
        return None

@st.cache_data
def load_data():
    """Loads all necessary parquet files from the presentation layer."""
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
            
    df_dict['fact_sales']['OrderDate'] = pd.to_datetime(df_dict['fact_sales']['OrderDate'])
    df_dict['dim_date']['Date'] = pd.to_datetime(df_dict['dim_date']['Date'])
    
    return df_dict

rates = get_exchange_rates()
dataframes = load_data()

if rates and dataframes:
    fact_sales = dataframes["fact_sales"]
    dim_customer = dataframes["dim_customer"]
    dim_product = dataframes["dim_product"]
    dim_employee = dataframes["dim_employee"]
    dim_date = dataframes["dim_date"]

    # --- SIDEBAR ---
    st.sidebar.image("logo.png", width=150)
    st.sidebar.header("VeloNorth Analytics")
    st.sidebar.title("Dashboard Filters")

    # Currency Selector
    currency_options = list(rates.keys())
    # Default to CAD if available, otherwise USD
    default_currency_index = currency_options.index("CAD") if "CAD" in currency_options else currency_options.index("USD")
    selected_currency = st.sidebar.selectbox("Select Currency", options=currency_options, index=default_currency_index)
    currency_symbol = currency_symbols.get(selected_currency, selected_currency) # Get the symbol

    min_date, max_date = dim_date['Date'].min().date(), dim_date['Date'].max().date()
    date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    all_countries = sorted(dim_customer['COUNTRY'].unique())
    selected_countries = st.sidebar.multiselect("Select Country", options=all_countries, default=all_countries)

    if 'SHORT_DESCR_y' in dim_product.columns:
        all_categories = sorted(dim_product['SHORT_DESCR_y'].unique())
        selected_categories = st.sidebar.multiselect("Select Product Category", options=all_categories, default=all_categories)
    else:
        selected_categories = []

    partner_role_map = {'1': 'Reseller', '2': 'Direct Customer'}
    dim_customer['Channel'] = dim_customer['PARTNERROLE'].map(partner_role_map).fillna('Unknown')
    all_channels = sorted(dim_customer['Channel'].unique())
    selected_channels = st.sidebar.multiselect("Select Sales Channel", options=all_channels, default=all_channels)

    # --- FILTERING DATA ---
    start_date, end_date = date_range
    status_col_case_insensitive = next((col for col in fact_sales.columns if col.lower() == 'lifecyclestatus'), None)
    
    if not status_col_case_insensitive:
        st.error("LifecycleStatus column not found. Please re-run the data pipeline.")
        st.stop()
        
    filtered_sales = fact_sales[(fact_sales['OrderDate'].dt.date >= start_date) & (fact_sales['OrderDate'].dt.date <= end_date)]
    
    filtered_sales = pd.merge(filtered_sales, dim_customer[['PARTNERID', 'COUNTRY', 'Channel', 'COMPANYNAME']], on='PARTNERID', how='left')
    
    if 'SHORT_DESCR_y' in dim_product.columns:
        filtered_sales = pd.merge(filtered_sales, dim_product[['PRODUCTID', 'SHORT_DESCR_y']], on='PRODUCTID', how='left')
        if selected_categories:
            filtered_sales = filtered_sales[filtered_sales['SHORT_DESCR_y'].isin(selected_categories)]

    if selected_countries:
        filtered_sales = filtered_sales[filtered_sales['COUNTRY'].isin(selected_countries)]
    if selected_channels:
        filtered_sales = filtered_sales[filtered_sales['Channel'].isin(selected_channels)]

    # --- DYNAMIC CURRENCY CONVERSION ---
    def convert_currency(row):
        from_currency_rate = rates.get(row['CURRENCY'], 1)
        to_currency_rate = rates.get(selected_currency, 1)
        # Avoid division by zero if a rate is missing or zero
        if from_currency_rate == 0: return 0
        return row['NETAMOUNT'] * (to_currency_rate / from_currency_rate)

    filtered_sales['ConvertedNetAmount'] = filtered_sales.apply(convert_currency, axis=1)


    # --- MAIN PAGE ---
    st.title(f"VeloNorth Sales Analytics ({selected_currency})")
    st.markdown("---")

    # --- KPIs based on Completed Sales and Converted Currency ---
    completed_sales = filtered_sales[filtered_sales[status_col_case_insensitive] == 'C']

    total_revenue = completed_sales['ConvertedNetAmount'].sum()
    total_orders = completed_sales['SALESORDERID'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    total_quantity = completed_sales['QUANTITY'].sum()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(label="Total Net Revenue", value=f"{currency_symbol}{total_revenue:,.2f}")
    kpi2.metric(label="Total Completed Orders", value=f"{total_orders:,}")
    kpi3.metric(label="Avg. Order Value", value=f"{currency_symbol}{avg_order_value:,.2f}")
    kpi4.metric(label="Total Quantity Sold", value=f"{total_quantity:,}")
    
    st.markdown("---")

    # --- CHARTS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Net Revenue by Product Category")
        if 'SHORT_DESCR_y' in filtered_sales.columns:
            revenue_by_category = filtered_sales.groupby('SHORT_DESCR_y')['ConvertedNetAmount'].sum().sort_values(ascending=False).reset_index()
            fig_cat = px.bar(
                revenue_by_category.head(10), x='ConvertedNetAmount', y='SHORT_DESCR_y', orientation='h',
                labels={'ConvertedNetAmount': f'Total Net Revenue ({currency_symbol})', 'SHORT_DESCR_y': 'Product Category'}, template='plotly_white'
            )
            fig_cat.update_layout(yaxis={'categoryorder':'total ascending'}, title_text='Top 10 Product Categories by Net Revenue')
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.warning("Product Category information not available.")

    with col2:
        st.subheader("Net Revenue by Sales Channel")
        revenue_by_channel = filtered_sales.groupby('Channel')['ConvertedNetAmount'].sum().reset_index()
        fig_channel = px.pie(
            revenue_by_channel, values='ConvertedNetAmount', names='Channel',
            title='Net Revenue Distribution by Sales Channel', hole=.4, template='plotly_white'
        )
        st.plotly_chart(fig_channel, use_container_width=True)

    st.markdown("### Monthly Net Revenue Trend")
    sales_over_time = filtered_sales.set_index('OrderDate').resample('ME')['ConvertedNetAmount'].sum().reset_index()
    fig_time = px.line(
        sales_over_time, x='OrderDate', y='ConvertedNetAmount',
        title='Monthly Net Revenue', labels={'ConvertedNetAmount': f'Total Net Revenue ({currency_symbol})', 'OrderDate': 'Month'}, template='plotly_white'
    )
    fig_time.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig_time, use_container_width=True)
    
    st.markdown("---")
    
    # --- DETAILED ANALYSIS ROW ---
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Top 10 Customers by Net Revenue")
        top_customers = filtered_sales.groupby('COMPANYNAME')['ConvertedNetAmount'].sum().sort_values(ascending=False).reset_index().head(10)
        st.dataframe(top_customers)
        
    with col4:
        st.subheader("Order Status Analysis")
        status_counts = filtered_sales.groupby(status_col_case_insensitive)['SALESORDERID'].nunique().reset_index()
        status_counts.rename(columns={'SALESORDERID': 'Order Count', status_col_case_insensitive: 'Lifecycle Status'}, inplace=True)
        fig_status = px.bar(
            status_counts, x='Lifecycle Status', y='Order Count',
            title='Order Count by Lifecycle Status', labels={'Lifecycle Status': 'Status Code', 'Order Count': 'Number of Orders'},
            template='plotly_white', text='Order Count'
        )
        st.plotly_chart(fig_status, use_container_width=True)

else:
    st.warning("Data could not be loaded. Please ensure the data pipeline has been run successfully.")

