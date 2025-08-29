from src.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from src.pipeline.stage_02_data_validation import DataValidationPipeline
from src.pipeline.stage_03_data_transformation import DataTransformationPipeline
from src.pipeline.stage_04_data_modelling import DataModellingPipeline
from src.logger_config import logger

STAGE_NAME = "Data Ingestion stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e


# --- STAGE 2: DATA VALIDATION ---
STAGE_NAME = "Data Validation stage"
try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<") 
    data_validation = DataValidationPipeline()
    data_validation.main()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

# --- STAGE 3: DATA TRANSFORMATION ---
STAGE_NAME = "Data Transformation stage"
try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<") 
    data_transformation = DataTransformationPipeline()
    data_transformation.main()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e


# --- STAGE 4: DATA MODELLING ---
STAGE_NAME = "Data Modelling stage"
try:
    logger.info(f">>>>>> Stage {STAGE_NAME} started <<<<<<") 
    data_modelling = DataModellingPipeline()
    data_modelling.main()
    logger.info(f">>>>>> Stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
