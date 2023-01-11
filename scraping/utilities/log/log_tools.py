import logging
from pathlib import Path

import scraping.utilities.web.config_objects as config

all_loggers: list[logging.getLoggerClass()] = []


def init_loggers():
    """
    Function that runs the necessary commands to set up the loggers.
    All logs go through the root logger StreamHandler and file handler.
    The root file handler only saves warning messages or higher.
    """
    logging_path = config.default_path_logging

    logs_path = logging_path.split("log_files")[0]
    Path(logs_path).mkdir(parents=True, exist_ok=True)
    log_path = f"{logs_path}/log_files"
    txt_path = f"{logs_path}/txt_files"
    Path(log_path).mkdir(parents=True, exist_ok=True)
    Path(txt_path).mkdir(parents=True, exist_ok=True)

    # --- Root logger ---
    # Root logger has level NOTSET, all messages that the sub-loggers want to pass along will be passed along.
    # Check https://docs.python.org/3/library/logging.html#logging.Logger.setLevel for details
    root_handler_stream = logging.StreamHandler()

    root_handler_file = logging.FileHandler(f"{log_path}/logging_global.log")
    root_handler_file.setLevel(logging.ERROR)

    logging.basicConfig(handlers=[root_handler_stream, root_handler_file])
    # ---

    # --- Logging module of the web scraper ---
    web_name = "web_scraper"
    log_web = logging.getLogger(web_name)
    log_web.setLevel(logging.INFO)

    log_web_handler_file = logging.FileHandler(f"{log_path}/logging_{web_name}.log")
    log_web.addHandler(log_web_handler_file)

    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)  # Avoid urllib3 DEBUG messages

    # Create logging module for all other modules
    logging_names = ["pdf_parser", "annex_10_parser", "annex_comparer","xml_converter", "combiner", "transformer", "db_communicator",
                     "utils_xml_comparer", "safe_io"]
    for log_name in logging_names:
        log = logging.getLogger(log_name)

        log_file_handler = logging.FileHandler(f"{log_path}/logging_{log_name}.log")
        log.addHandler(log_file_handler)

        all_loggers.append(log)

    set_level_loggers(config.logging_level)


def set_level_loggers(log_level: int):
    """
    Set the level of all the submodule loggers to the specified level.
    The logging level is an integer, but it is better to specify these as logger levels as they are specified in the
    logging module. Check https://docs.python.org/3/library/logging.html#logging-levels for details.

    Args:
        log_level (int): Logging level to use. For clarity, use a value like `logging.DEBUG`.
    """
    for logging_obj in all_loggers:
        logging_obj.setLevel(log_level)


def get_log_path(filename: str, data_path: str) -> str:
    """
    Args:
        filename (str): Name of the logging file
        data_path (str): Path of the data folder

    Returns:
        str: Path of the location of the logging file, based on whether the main or tests are being run
    """
    if "test" in data_path:
        parent_path = "/".join((data_path.strip('/').split('/')[:-2]))
        if ".log" in filename:
            return f"{parent_path}/tests/logs/log_files/{filename}"
        elif ".txt" in filename:
            return f"{parent_path}/tests/logs/txt_files/{filename}"
    else:
        parent_path = "/".join((data_path.strip('/').split('/')[:-1]))
        if ".log" in filename:
            return f"{parent_path}/logs/log_files/{filename}"
        elif ".txt" in filename:
            return f"{parent_path}/logs/txt_files/{filename}"
