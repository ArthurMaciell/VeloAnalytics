import os
from pathlib import Path
from src.logging import logger
from src.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        """
        Initializes the DataValidation component with its configuration.
        """
        self.config = config

    def validate_all_files_exist(self) -> bool:
        """
        Validates that all expected files exist in the unzipped data directory.
        For this project, we expect 9 CSV files.
        """
        try:
            validation_status = True
            
            # Get a list of all files in the directory
            all_files = os.listdir(self.config.unzip_data_dir)
            
            # For this specific challenge, we know there should be 9 CSV files.
            # A more robust solution could take a list of required files from the config.
            expected_file_count = 9
            
            if len(all_files) != expected_file_count:
                validation_status = False
                logger.warning(f"File count validation failed. Expected {expected_file_count} files, but found {len(all_files)}.")
            else:
                logger.info(f"File count validation successful. Found {len(all_files)} files.")

            # Write the final validation status to the status file
            with open(self.config.status_file, "w") as f:
                f.write(f"Validation status: {validation_status}")
            
            return validation_status

        except Exception as e:
            logger.error(f"An error occurred during file validation: {e}")
            # Ensure status is written as false if an error occurs
            with open(self.config.status_file, "w") as f:
                f.write(f"Validation status: False")
            return False
