import logging
import os


def init_loggers(logging_path: str = "../logs/log_files") -> None:
    """
    Function that runs the necessary commands to set up the loggers.
    All logs go through the root logger StreamHandler and file handler.
    The root file handler only saves warning messages or higher.

    Args:
        logging_path (str): Path in which the log files will be saved.
    """
    if not os.path.isdir(logging_path):
        os.mkdir(logging_path)

    # --- Root logger ---
    root_handler_stream = logging.StreamHandler()

    root_handler_file = logging.FileHandler(f"{logging_path}/logging_global.log")
    root_handler_file.setLevel(logging.ERROR)

    logging.basicConfig(level=logging.INFO, handlers=[root_handler_stream, root_handler_file])
    # ---

    # --- Logging module of the web scraper ---
    web_name = "web_scraper"
    log_web = logging.getLogger(web_name)
    log_web.setLevel(logging.INFO)

    log_web_handler_file = logging.FileHandler(f"{logging_path}/logging_{web_name}.log")
    log_web.addHandler(log_web_handler_file)

    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)  # Avoid urllib3 DEBUG messages
    # ---

    # Create logging module for all other modules
    logging_names = ["pdf_parser", "xml_converter", "annex_10_parser", "safe_io"]
    for log_name in logging_names:
        log = logging.getLogger(log_name)
        log.setLevel(logging.INFO)

        log_file_handler = logging.FileHandler(f"{logging_path}/logging_{log_name}.log")
        log.addHandler(log_file_handler)


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
