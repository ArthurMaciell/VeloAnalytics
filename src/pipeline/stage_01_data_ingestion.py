from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.logger_config import logger

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionPipeline:
    def __init__(self):
        """
        This pipeline is responsible for orchestrating the data ingestion process.
        """
        pass

    def main(self):
        """
        The main method to execute the data ingestion stage.
        It gets the configuration, initializes the data ingestion component,
        and runs the unzipping process.
        """
        try:
            logger.info(f">>>>>> Stage '{STAGE_NAME}' started <<<<<<")
            
            # Initialize the configuration manager
            config = ConfigurationManager()
            
            # Get the specific configuration for data ingestion
            data_ingestion_config = config.get_data_ingestion_config()
            
            # Initialize the data ingestion component with the configuration
            data_ingestion = DataIngestion(config=data_ingestion_config)
            
            # Run the unzipping process
            data_ingestion.unzip_source_file()
            
            logger.info(f">>>>>> Stage '{STAGE_NAME}' completed successfully <<<<<<\n\nx==========x")
            
        except Exception as e:
            logger.exception(e)
            raise e

# This block allows you to run this pipeline stage directly as a script
if __name__ == '__main__':
    try:
        pipeline = DataIngestionPipeline()
        pipeline.main()
    except Exception as e:
        logger.exception(f"The Data Ingestion pipeline failed with error: {e}")
        raise e
