from src.config.configuration import ConfigurationManager
from src.components.data_validation import DataValidation
from src.logger_config import logger

STAGE_NAME = "Data Validation Stage"

class DataValidationPipeline:
    def __init__(self):
        """
        This pipeline is responsible for orchestrating the data validation process.
        """
        pass

    def main(self):
        """
        The main method to execute the data validation stage.
        """
        try:
            logger.info(f">>>>>> Stage '{STAGE_NAME}' started <<<<<<")
            
            # Initialize the configuration manager
            config = ConfigurationManager()
            
            # Get the specific configuration for data validation
            data_validation_config = config.get_data_validation_config()
            
            # Initialize the data validation component with the configuration
            data_validation = DataValidation(config=data_validation_config)
            
            # Run the validation process
            data_validation.validate_all_files_exist()
            
            logger.info(f">>>>>> Stage '{STAGE_NAME}' completed successfully <<<<<<\n\nx==========x")
            
        except Exception as e:
            logger.exception(e)
            raise e

# This block allows you to run this pipeline stage directly as a script
if __name__ == '__main__':
    try:
        pipeline = DataValidationPipeline()
        pipeline.main()
    except Exception as e:
        logger.exception(f"The Data Validation pipeline failed with error: {e}")
        raise e
