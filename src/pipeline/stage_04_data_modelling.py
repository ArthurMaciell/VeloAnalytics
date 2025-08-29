from src.config.configuration import ConfigurationManager
from src.components.data_modelling import DataModelling
from src.logger_config import logger

STAGE_NAME = "Data Modelling Stage"

class DataModellingPipeline:
    def __init__(self):
        """
        This pipeline is responsible for orchestrating the data modelling process.
        """
        pass

    def main(self):
        """
        The main method to execute the data modelling stage.
        """
        try:
            logger.info(f">>>>>> Stage '{STAGE_NAME}' started <<<<<<")
            
            # Initialize the configuration manager
            config = ConfigurationManager()
            
            # Get the specific configuration for data modelling
            data_modelling_config = config.get_data_modelling_config()
            
            # Initialize the data modelling component with the configuration
            data_modelling = DataModelling(config=data_modelling_config)
            
            # Run the star schema building process
            data_modelling.build_star_schema()
            
            logger.info(f">>>>>> Stage '{STAGE_NAME}' completed successfully <<<<<<\n\nx==========x")
            
        except Exception as e:
            logger.exception(e)
            raise e

# This block allows you to run this pipeline stage directly as a script
if __name__ == '__main__':
    try:
        pipeline = DataModellingPipeline()
        pipeline.main()
    except Exception as e:
        logger.exception(f"The Data Modelling pipeline failed with error: {e}")
        raise e
