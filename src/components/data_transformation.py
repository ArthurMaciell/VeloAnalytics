import os
import pandas as pd
from pathlib import Path
from src.logging import logger
from src.entity.config_entity import DataTransformationConfig
from src.utils import read_yaml

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        """
        Initializes the DataTransformation component with its configuration.
        """
        self.config = config
        self.schema = read_yaml(Path("schema.yaml"))

    def validate_and_transform_data(self):
        """
        Reads all raw CSV files, validates them against the defined schema,
        and saves them as processed Parquet files.
        """
        try:
            data_files = os.listdir(self.config.data_path)
            csv_files = [f for f in data_files if f.endswith('.csv')]
            logger.info(f"Found {len(csv_files)} CSV files to transform.")

            for csv_file in csv_files:
                file_name = Path(csv_file).stem # Gets the file name without extension (e.g., 'Products')
                
                if file_name not in self.schema.COLUMNS:
                    logger.warning(f"Schema not defined for {csv_file}. Skipping this file.")
                    continue

                logger.info(f"Processing and validating file: {csv_file}")
                
                # Define schema and read csv
                file_schema = self.schema.COLUMNS[file_name]
                df = pd.read_csv(os.path.join(self.config.data_path, csv_file))

                # Validate columns
                validation_errors = []
                for col in file_schema.keys():
                    if col not in df.columns:
                        validation_errors.append(col)
                
                if validation_errors:
                    logger.error(f"Schema validation failed for {csv_file}. Missing columns: {validation_errors}")
                    # In a real-world scenario, you might raise an error here or move the file to a quarantine folder.
                    # For this challenge, we will log the error and continue.
                    continue
                
                # (Optional) Here you would add more transformation logic:
                # - Enforce data types from schema
                # - Handle missing values
                # - Create new features

                # Save the processed dataframe as a parquet file
                output_file_path = os.path.join(self.config.output_path, f"{file_name}.parquet")
                df.to_parquet(output_file_path, index=False)
                logger.info(f"Successfully transformed and saved {csv_file} to {output_file_path}")

        except Exception as e:
            logger.exception(f"An error occurred during data transformation: {e}")
            raise e
