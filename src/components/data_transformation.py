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

    def _clean_and_transform(self, df: pd.DataFrame, file_schema: dict) -> pd.DataFrame:
        """
        Private helper method to apply cleaning and transformations to a dataframe.
        """
        # --- 1. Enforce Data Types based on schema.yaml ---
        for col, dtype in file_schema.items():
            if col in df.columns:
                if 'date' in col.lower() or 'at' in col.lower():
                    df[col] = pd.to_datetime(df[col], format='%Y%m%d', errors='coerce')
                else:
                    df[col] = df[col].astype(dtype, errors='ignore')
        
        # --- 2. Handle Missing Values ---
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

                # --- FIX: Clean column names to remove BOM and other issues ---
                df.columns = df.columns.str.replace('ï»¿', '', regex=False).str.strip()

                # --- Schema Column Validation ---
                schema_cols = set(file_schema.keys())
                df_cols = set(df.columns)
                
                if not schema_cols.issubset(df_cols):
                    missing_cols = schema_cols - df_cols
                    logger.error(f"Schema validation failed for {csv_file}. Missing columns: {missing_cols}")
                    continue
                
                # --- Apply Cleaning and Transformations ---
                df_transformed = self._clean_and_transform(df, file_schema)

                # --- Save the processed dataframe as a parquet file ---
                output_file_path = os.path.join(processed_data_path, f"{file_name}.parquet")
                df_transformed.to_parquet(output_file_path, index=False)
                logger.info(f"Successfully transformed and saved {csv_file} to {output_file_path}")

        except Exception as e:
            logger.exception(f"An error occurred during data transformation: {e}")
            raise e