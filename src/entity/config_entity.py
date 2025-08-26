from dataclasses import dataclass
from pathlib import Path

# --- Data Ingestion Configuration Entity ---
# This defines the structure for the data ingestion configuration.
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_zip_file: Path
    unzip_dir: Path


# --- Data Validation Configuration Entity ---
# This defines the structure for the data validation configuration.
@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    unzip_data_dir: Path
    status_file: Path
