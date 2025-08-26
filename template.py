import os
from pathlib import Path
import logging

# Basic logging configuration to track the setup process
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s'
)

# Project name (you can choose from the suggestions or create your own)
project_name = "VeloAnalytics"

# List of files and directories based on the professional project structure
list_of_items = [
    ".github/workflows/.gitkeep",
    "data/01_raw/.gitkeep",
    "data/02_processed/.gitkeep",
    "data/03_presentation/.gitkeep",
    "docs/01_data_quality_report.md",
    "docs/02_data_model_diagram.png", # This is a placeholder, you will replace the image
    "notebooks/01_initial_exploration.ipynb",
    "notebooks/02_data_cleaning_and_validation.ipynb",
    "notebooks/03_data_modeling.ipynb",
    f"src/__init__.py",
    f"src/data_processing.py",
    f"src/metrics.py",
    f"src/utils.py",
    f"src/app.py",
    ".gitignore",
    "config.yaml",
    "README.md",
    "requirements.txt"
]

# Loop to create the directory structure
for item_path_str in list_of_items:
    item_path = Path(item_path_str)
    item_dir, item_name = os.path.split(item_path)

    # 1. Create the directory if it doesn't exist
    if item_dir != "":
        os.makedirs(item_dir, exist_ok=True)
        logging.info(f"Creating directory: {item_dir}")

    # 2. Create the file if it doesn't exist or is empty
    if not item_path.exists() or item_path.stat().st_size == 0:
        with open(item_path, 'w') as f:
            pass # Create an empty file
        logging.info(f"Creating file: {item_path}")
    else:
        logging.info(f"File {item_path} already exists.")

logging.info(f"Project structure for '{project_name}' created successfully!")

# Adding initial content to important files
try:
    with open("README.md", "w") as f:
        f.write(f"# {project_name} - BI & Data Modelling Technical Challenge\n\n")
        f.write("This repository contains the solution for the technical challenge...\n")

    with open("requirements.txt", "w") as f:
        f.write("pandas\n")
        f.write("numpy\n")
        f.write("streamlit\n")
        f.write("plotly\n")
        f.write("pyarrow\n") # For working with parquet files
        f.write("python-dotenv\n")
        f.write("PyYAML\n")


    logging.info("Initialized README.md, requirements.txt, and .gitignore files.")
except Exception as e:
    logging.error(f"Error while initializing config files: {e}")
