import web_scraper.__main__ as m
import logging

log_handler_console = logging.StreamHandler()
log_handler_file = logging.FileHandler("webscraper.log")

logging.basicConfig(level=logging.INFO, handlers=[log_handler_console, log_handler_file])
m.log = logging.getLogger("webscraper")
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)