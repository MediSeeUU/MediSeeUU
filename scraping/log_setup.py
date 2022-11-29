import logging
import scraping.config_objects as config


all_loggers: list[logging.getLoggerClass()] = []


def init_loggers():
    """
    Function that runs the necessary commands to set up the loggers.
    All logs go through the root logger StreamHandler and file handler.
    The root file handler only saves warning messages or higher.

    Returns: None
    """
    logger_name_web: str = "web_scraper"
    logger_name_pdf: str = "pdf_parser"

    # --- Root logger ---
    # Root logger has level NOTSET, all messages that the sub-loggers want to pass along will be passed along.
    # Check https://docs.python.org/3/library/logging.html#logging.Logger.setLevel for details
    root_handler_stream = logging.StreamHandler()

    root_handler_file = logging.FileHandler(f"{config.default_path_logging}/logging_global.log")
    root_handler_file.setLevel(logging.ERROR)

    logging.basicConfig(handlers=[root_handler_stream, root_handler_file])
    # ---

    # --- Logging module of the web scraper ---
    log_web = logging.getLogger(logger_name_web)

    log_web_handler_file = logging.FileHandler(f"{config.default_path_logging}/logging_{logger_name_web}.log")
    log_web.addHandler(log_web_handler_file)

    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)  # Avoid urllib3 DEBUG messages
    # ---

    # --- Logging module of the PDF parser ---
    log_pdf = logging.getLogger(logger_name_pdf)

    log_pdf_file_handler = logging.FileHandler(f"{config.default_path_logging}/logging_{logger_name_pdf}.log")
    log_pdf.addHandler(log_pdf_file_handler)
    # ---

    # -- Set levels of all loggers
    all_loggers.append(log_web)
    all_loggers.append(log_pdf)
    set_level_loggers(config.logging_level)
    # ---


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
