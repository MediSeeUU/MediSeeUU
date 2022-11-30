import logging
import os
import scraping.utilities.web.config_objects as config


all_loggers: list[logging.getLoggerClass()] = []


def init_loggers():
    """
    Function that runs the necessary commands to set up the loggers.
    All logs go through the root logger StreamHandler and file handler.
    The root file handler only saves warning messages or higher.

    Returns: None
    """
    if not os.path.isdir(config.default_path_logging):
        os.mkdir(config.default_path_logging)

    web_name: str = "web_scraper"
    pdf_name: str = "pdf_parser"
    xml_name: str = "xml_converter"
    annex_10_name: str = "annex_10_parser"

    # --- Root logger ---
    # Root logger has level NOTSET, all messages that the sub-loggers want to pass along will be passed along.
    # Check https://docs.python.org/3/library/logging.html#logging.Logger.setLevel for details
    root_handler_stream = logging.StreamHandler()

    root_handler_file = logging.FileHandler(f"{config.default_path_logging}/logging_global.log")
    root_handler_file.setLevel(logging.ERROR)

    logging.basicConfig(handlers=[root_handler_stream, root_handler_file])
    # ---

    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)  # Avoid urllib3 DEBUG messages

    # Create logging module for all other modules
    logging_names = [web_name, pdf_name, xml_name, annex_10_name]
    for log_name in logging_names:
        log = logging.getLogger(log_name)

        log_file_handler = logging.FileHandler(f"{config.default_path_logging}/logging_{log_name}.log")
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

    Returns: None
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
    parent_path = "/".join((data_path.strip('/').split('/')[:-1]))
    if "test" in data_path:
        if ".log" in filename:
            return f"{parent_path}/tests/logs/log_files/{filename}"
        elif ".txt" in filename:
            return f"{parent_path}/tests/logs/txt_files/{filename}"
    else:
        if ".log" in filename:
            return f"{parent_path}/logs/log_files/{filename}"
        elif ".txt" in filename:
            return f"{parent_path}/logs/txt_files/{filename}"
