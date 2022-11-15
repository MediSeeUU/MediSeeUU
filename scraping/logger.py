import logging


class PDFLogger:
    """
    Create logger for writing log messages and saving them to a file.
    Here, thile file is pdf_scraper.log
    """
    log_handler_console = logging.StreamHandler()
    log_handler_file = logging.FileHandler("pdf_scraper.log")
    logging.basicConfig(level=logging.INFO, handlers=[log_handler_console, log_handler_file])
    log = logging.getLogger("pdf_scraper")


class WebLogger:
    """
    Create logger for writing log messages and saving them to a file.
    Here, thile file is web_scraper.log
    """
    log_handler_console = logging.StreamHandler()
    log_handler_file = logging.FileHandler("web_scraper.log")
    logging.basicConfig(level=logging.INFO, handlers=[log_handler_console, log_handler_file])
    log = logging.getLogger("web_scraper")
    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)
