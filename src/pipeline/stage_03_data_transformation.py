from src.config.configuration import ConfigurationManager
from src.components.data_transformation import DataTransformation
from src.logger_config import logger

STAGE_NAME = "Data Transformation Stage"

class DataTransformationPipeline:
    def __init__(self):
        """
        This pipeline is responsible for orchestrating the data transformation process.
        """
        pass

    def main(self):
        """
        The main method to execute the data transformation stage.
        """
        try:
            logger.info(f">>>>>> Stage '{STAGE_NAME}' started <<<<<<")
            
            # Initialize the configuration manager
            config = ConfigurationManager()
            
            # Get the specific configuration for data transformation
            data_transformation_config = config.get_data_transformation_config()
            
            # Initialize the data transformation component
            data_transformation = DataTransformation(config=data_transformation_config)
            
            # Run the transformation process
            data_transformation.validate_and_transform_data()
            
            logger.info(f">>>>>> Stage '{STAGE_NAME}' completed successfully <<<<<<\n\nx==========x")
            
        except Exception as e:
            logger.exception(e)
            raise e

# This block allows you to run this pipeline stage directly as a script
if __name__ == '__main__':
    try:
        pipeline = DataTransformationPipeline()
        pipeline.main()
    except Exception as e:
        logger.exception(f"The Data Transformation pipeline failed with error: {e}")
        raise e
