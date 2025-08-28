import os
import pandas as pd
from pathlib import Path
from src.logging import logger
from src.entity.config_entity import DataModellingConfig

class DataModelling:
    def __init__(self, config: DataModellingConfig):
        """
        Initializes the DataModelling component with its configuration.
        """
        self.config = config

    def _load_processed_data(self) -> dict:
        """
        Loads all processed Parquet files into a dictionary of pandas DataFrames.
        """
        dataframes = {}
        path = self.config.processed_data_path
        for file_name in os.listdir(path):
            if file_name.endswith('.parquet'):
                table_name = Path(file_name).stem
                dataframes[table_name] = pd.read_parquet(os.path.join(path, file_name))
        logger.info(f"Loaded {len(dataframes)} processed tables.")
        return dataframes

    def build_star_schema(self):
        """
        Builds the fact and dimension tables for the star schema.
        """
        try:
            logger.info("Starting the data modelling process to build the star schema.")
            df_dict = self._load_processed_data()

            # --- 1. Build dim_customer ---
            df_partners = df_dict['BusinessPartners']
            df_addresses = df_dict['Addresses']
            dim_customer = pd.merge(df_partners, df_addresses, on='ADDRESSID', how='left')
            
            # --- 2. Build dim_product ---
            df_products = df_dict['Products']
            df_prod_cat_text = df_dict['ProductCategoryText']
            df_prod_text = df_dict['ProductTexts']
            
            df_prod_cat_text = df_prod_cat_text[df_prod_cat_text['LANGUAGE'] == 'EN']
            df_prod_text = df_prod_text[df_prod_text['LANGUAGE'] == 'EN']
            
            dim_product_intermediate = pd.merge(df_products, df_prod_cat_text, on='PRODCATEGORYID', how='left')
            dim_product = pd.merge(dim_product_intermediate, df_prod_text, on='PRODUCTID', how='left')

            # --- 3. Build dim_employee ---
            dim_employee = df_dict['Employees']

            # --- 4. Build dim_date ---
            df_sales_orders = df_dict['SalesOrders']
            df_sales_orders['CREATEDAT'] = pd.to_datetime(df_sales_orders['CREATEDAT'])
            min_date = df_sales_orders['CREATEDAT'].min()
            max_date = df_sales_orders['CREATEDAT'].max()
            
            dim_date = pd.DataFrame({'Date': pd.date_range(min_date, max_date)})
            dim_date['Year'] = dim_date['Date'].dt.year
            dim_date['Month'] = dim_date['Date'].dt.month
            dim_date['Day'] = dim_date['Date'].dt.day
            dim_date['Quarter'] = dim_date['Date'].dt.quarter
            dim_date['DayOfWeek'] = dim_date['Date'].dt.dayofweek # Monday=0, Sunday=6

            # --- 5. Build fact_sales (Further enriched with your suggestion) ---
            df_sales_items = df_dict['SalesOrderItems']
            
            # Select columns to enrich the fact table from the main order table
            order_details = df_sales_orders[[
                'SALESORDERID', 'PARTNERID', 'CREATEDBY', 
                'CREATEDAT', 'BILLINGSTATUS', 'DELIVERYSTATUS', 'LIFECYCLESTATUS'
            ]]
            
            fact_sales = pd.merge(df_sales_items, order_details, on='SALESORDERID', how='left')
            
            # Rename columns for clarity in the final model
            fact_sales.rename(columns={
                'CREATEDAT': 'OrderDate', 
                'CREATEDBY': 'EMPLOYEEID',
                'BILLINGSTATUS': 'BillingStatus',
                'DELIVERYSTATUS': 'DeliveryStatus',
                'LIFECYCLESTATUS': 'LifecycleStatus'
            }, inplace=True)
            
            # --- 6. Save Presentation Tables ---
            presentation_path = self.config.presentation_path
            dim_customer.to_parquet(os.path.join(presentation_path, "dim_customer.parquet"), index=False)
            dim_product.to_parquet(os.path.join(presentation_path, "dim_product.parquet"), index=False)
            dim_employee.to_parquet(os.path.join(presentation_path, "dim_employee.parquet"), index=False)
            dim_date.to_parquet(os.path.join(presentation_path, "dim_date.parquet"), index=False)
            fact_sales.to_parquet(os.path.join(presentation_path, "fact_sales.parquet"), index=False)
            
            logger.info(f"Successfully built and saved star schema tables to '{presentation_path}'")

        except Exception as e:
            logger.error(f"An error occurred during data modelling: {e}")
            raise e
