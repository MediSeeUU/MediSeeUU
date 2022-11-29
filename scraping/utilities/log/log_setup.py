import logging


def init_loggers(logging_path: str = "../logs/log_files") -> None:
    """
    Function that runs the necessary commands to set up the loggers.
    All logs go through the root logger StreamHandler and file handler.
    The root file handler only saves warning messages or higher.

    Args:
        logging_path (str): Path in which the log files will be saved.

    Returns: None

    """
    web_name: str = "web_scraper"
    pdf_name: str = "pdf_parser"
    xml_name: str = "xml_converter"

    # --- Root logger ---
    root_handler_stream = logging.StreamHandler()

    root_handler_file = logging.FileHandler(f"{logging_path}/logging_global.log")
    root_handler_file.setLevel(logging.ERROR)

    logging.basicConfig(level=logging.INFO, handlers=[root_handler_stream, root_handler_file])
    # ---

    # --- Logging module of the web scraper ---
    log_web = logging.getLogger(web_name)
    log_web.setLevel(logging.INFO)

    log_web_handler_file = logging.FileHandler(f"{logging_path}/logging_{web_name}.log")
    log_web.addHandler(log_web_handler_file)

    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)  # Avoid urllib3 DEBUG messages
    # ---

    # --- Logging module of the PDF parser ---
    log_pdf = logging.getLogger(pdf_name)
    log_pdf.setLevel(logging.INFO)

    log_pdf_file_handler = logging.FileHandler(f"{logging_path}/logging_{pdf_name}.log")
    log_pdf.addHandler(log_pdf_file_handler)
    # ---

    # --- Logging module of the XML converter ---
    log_xml = logging.getLogger(xml_name)
    log_xml.setLevel(logging.INFO)

    log_xml_file_handler = logging.FileHandler(f"{logging_path}/logging_{xml_name}.log")
    log_xml.addHandler(log_xml_file_handler)
    # ---
