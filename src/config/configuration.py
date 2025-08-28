from src.utils import read_yaml, create_directories
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, DataModellingConfig
from pathlib import Path

class ConfigurationManager:
    def __init__(
        self, 
        config_filepath = Path("config.yaml")):
        """
        Initializes the ConfigurationManager by reading the main config file.
        It also creates the main artifacts directory.
        """
        self.config = read_yaml(config_filepath)
        create_directories([Path(self.config.artifacts_root)])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Extracts the data ingestion configuration from the main config file,
        creates its specific artifact directory, and returns it as a 
        DataIngestionConfig object.
        """
        # Get the data_ingestion section from the config file
        config = self.config.data_ingestion

        # Create the specific directory for this component (e.g., artifacts/data_ingestion)
        create_directories([Path(config.root_dir)])

        # Create and return the structured configuration object using the blueprint from the entity file
        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_zip_file=Path(config.source_zip_file),
            unzip_dir=Path(config.unzip_dir)
        )

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Extracts the data validation configuration from the main config file,
        creates its specific artifact directory, and returns it as a 
        DataValidationConfig object.
        """
        config = self.config.data_validation
        create_directories([Path(config.root_dir)])

        data_validation_config = DataValidationConfig(
            root_dir=Path(config.root_dir),
            unzip_data_dir=Path(config.unzip_data_dir),
            status_file=Path(config.status_file)
        )
        return data_validation_config
    

    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Extracts the data transformation configuration from the main config file.
        """
        config = self.config.data_transformation
        create_directories([Path(config.root_dir), Path(config.output_path)])

        data_transformation_config = DataTransformationConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            output_path=Path(config.output_path)
        )
        return data_transformation_config

    def get_data_modelling_config(self) -> DataModellingConfig:
        """
        Extracts the data modelling configuration from the main config file.
        """
        config = self.config.data_modelling
        create_directories([Path(config.root_dir), Path(config.presentation_path)])

        data_modelling_config = DataModellingConfig(
            root_dir=Path(config.root_dir),
            processed_data_path=Path(config.processed_data_path),
            presentation_path=Path(config.presentation_path)
        )
        return data_modelling_config