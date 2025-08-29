import os
import yaml
from pathlib import Path
from typing import List
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from src.logger_config import logger # CORRECTED: Importing from our logging module

# --- File Operations ---

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its content as a ConfigBox object.
    ConfigBox allows accessing dictionary keys using dot notation (e.g., config.key).

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty or has a syntax error.
        Exception: For other file reading errors.

    Returns:
        ConfigBox: A ConfigBox object containing the file's content.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            if not content:
                raise ValueError("YAML file is empty.")
            logger.info(f"YAML file loaded successfully: {path_to_yaml}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file syntax error.")
    except Exception as e:
        logger.error(f"Error reading YAML file {path_to_yaml}: {e}")
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose: bool = True):
    """
    Creates a list of directories.

    Args:
        path_to_directories (List[Path]): A list of directory paths to create.
        verbose (bool, optional): If True, logs the creation of each directory. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created or already exists: {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    """
    Gets the size of a file and returns it as a formatted string in KB.

    Args:
        path (Path): Path of the file.

    Returns:
        str: The file size formatted as "~ {size} KB".
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"
