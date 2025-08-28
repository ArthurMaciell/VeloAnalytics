import os
import pandas as pd
from pathlib import Path
from src.logging import logger
from src.entity.config_entity import DataTransformationConfig
from src.utils import read_yaml

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        """
        Initializes the DataTransformation component with its configuration
        and loads the data schema.
        """
        self.config = config
        self.schema = read_yaml(Path("schema.yaml"))

    def _clean_and_transform(self, df: pd.DataFrame, file_schema: dict, file_name: str) -> pd.DataFrame:
        """
        Private helper method to apply cleaning and transformations to a dataframe.
        """
        # --- NEW: Select only the columns defined in the schema ---
        # This proactively drops any unexpected columns like "Unnamed: 13"
        df = df[list(file_schema.keys())].copy()
        
        # --- Drop Duplicates based on Primary Key defined in schema.yaml ---
        primary_keys_config = self.schema.get('PRIMARY_KEYS', {})
        primary_key = primary_keys_config.get(file_name)
        
        if primary_key:
            subset = primary_key if isinstance(primary_key, list) else [primary_key]
            initial_rows = len(df)
            df.drop_duplicates(subset=subset, keep='first', inplace=True)
            final_rows = len(df)
            if initial_rows > final_rows:
                logger.info(f"Dropped {initial_rows - final_rows} duplicate rows from {file_name} based on key(s): {subset}")

        # --- Enforce Data Types based on schema.yaml ---
        for col, dtype in file_schema.items():
            if col in df.columns:
                if 'date' in col.lower() or 'at' in col.lower():
                    df[col] = pd.to_datetime(df[col], format='%Y%m%d', errors='coerce')
                else:
                    df[col] = df[col].astype(dtype, errors='ignore')
        
        # --- Handle Missing Values ---
        for col in df.select_dtypes(include=['number']).columns:
            df[col] = df[col].fillna(0)
        for col in df.select_dtypes(include=['object', 'string']).columns:
            df[col] = df[col].fillna('N/A')
            
        return df

    def validate_and_transform_data(self):
        """
        Reads all raw CSV files, validates them against the defined schema,
        applies transformations, and saves them as processed Parquet files.
        """
        try:
            raw_data_path = self.config.data_path
            processed_data_path = self.config.output_path
            all_schemas = self.schema.COLUMNS

            all_csv_files = [f for f in os.listdir(raw_data_path) if f.endswith('.csv')]
            logger.info(f"Found {len(all_csv_files)} CSV files to transform.")

            for csv_file in all_csv_files:
                file_name = Path(csv_file).stem
                
                if file_name not in all_schemas:
                    logger.warning(f"Schema not defined for {csv_file}. Skipping.")
                    continue

                logger.info(f"Processing and validating file: {csv_file}")
                
                file_schema = all_schemas[file_name]
                df = pd.read_csv(os.path.join(raw_data_path, csv_file), encoding='latin1')
                df.columns = df.columns.str.replace('ï»¿', '', regex=False).str.strip()

                schema_cols = set(file_schema.keys())
                df_cols = set(df.columns)
                
                if not schema_cols.issubset(df_cols):
                    missing_cols = schema_cols - df_cols
                    logger.error(f"Schema validation failed for {csv_file}. Missing columns: {missing_cols}")
                    continue
                
                # Pass file_name to the helper method
                df_transformed = self._clean_and_transform(df, file_schema, file_name)

                output_file_path = os.path.join(processed_data_path, f"{file_name}.parquet")
                df_transformed.to_parquet(output_file_path, index=False)
                logger.info(f"Successfully transformed and saved {csv_file} to {output_file_path}")

        except Exception as e:
            logger.exception(f"An error occurred during data transformation: {e}")
            raise e