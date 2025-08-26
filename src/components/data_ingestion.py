import os
import zipfile
from pathlib import Path
from src.logging import logger
from src.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        """
        Initializes the DataIngestion component with its configuration.
        """
        self.config = config

    def unzip_source_file(self):
        """
        Unzips the source file into the specified directory from the configuration.
        """
        logger.info(f"Unzipping source file: {self.config.source_zip_file} into {self.config.unzip_dir}")
        
        # Ensure the target directory exists before unzipping
        os.makedirs(self.config.unzip_dir, exist_ok=True)
        
        with zipfile.ZipFile(self.config.source_zip_file, 'r') as zip_ref:
            zip_ref.extractall(self.config.unzip_dir)
            logger.info(f"Successfully unzipped file to {self.config.unzip_dir}")

