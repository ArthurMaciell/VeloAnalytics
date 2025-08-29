import os
import sys
import logging

# --- Logger Setup ---

# Define the log format
# Example: [2023-10-27 15:30:00: INFO: data_ingestion: Log message here]
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Define the log directory and file path
log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

# Configure the logger to have two handlers:
# 1. FileHandler: Saves logs to the running_logs.log file.
# 2. StreamHandler: Displays logs in the terminal during execution.
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create and export the logger instance to be used across the project
logger = logging.getLogger("VeloAnalyticsLogger")
