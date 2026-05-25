"""
===============================================================================
LOGGER UTILITY
===============================================================================

This file creates a reusable logger for the entire framework.

===============================================================================
"""

import logging
import os
from datetime import datetime


# =============================================================================
# FUNCTION : GET LOGGER
# =============================================================================

# Returns a logger object for a given module name
def get_logger(name: str) -> logging.Logger:

    """
    Create and return a configured logger.

    Args:
        name (str): Name of the logger (usually __name__)

    Returns:
        logging.Logger: Configured logger instance
    """

    # -------------------------------------------------------------------------
    # CREATE LOGS DIRECTORY
    # -------------------------------------------------------------------------

    # Logs will be stored inside /logs folder
    logs_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "logs"
    )

    # Create folder if it does not exist
    os.makedirs(logs_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # CREATE UNIQUE LOG FILE NAME (WITH TIMESTAMP)
    # -------------------------------------------------------------------------

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    log_file = os.path.join(
        logs_dir,
        f"world_population_count_check_{timestamp}.log"
    )

    # -------------------------------------------------------------------------
    # CREATE LOGGER OBJECT
    # -------------------------------------------------------------------------

    logger = logging.getLogger(name)

    # Avoid duplicate handlers if logger already exists
    if not logger.handlers:

        # Set lowest level to capture all logs
        logger.setLevel(logging.DEBUG)

        # ---------------------------------------------------------------------
        # LOG FORMAT
        # ---------------------------------------------------------------------

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # ---------------------------------------------------------------------
        # CONSOLE HANDLER
        # ---------------------------------------------------------------------

        # Shows logs in terminal (only INFO and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # ---------------------------------------------------------------------
        # FILE HANDLER
        # ---------------------------------------------------------------------


        # Writes logs into file (DEBUG and above)
        file_handler = logging.FileHandler(
            log_file,
            mode="a",
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Attach handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger