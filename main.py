from src.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from src.pipeline.stage_02_data_validation import DataValidationPipeline
from src.logging import logger

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