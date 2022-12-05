import json
from pathlib import Path
from datetime import datetime
import os
import multiprocessing
import logging


from scraping.web_scraper import download, ec_scraper, ema_scraper, filter_retry, save_webdata
from scraping.utilities.web.medicine_type import MedicineType
import scraping.utilities.log.log_tools as log_tools
from scraping.utilities.web import json_helper
import scraping.utilities.web.config_objects as config_objects
from scraping.web_scraper import url_scraper


log = logging.getLogger("web_scraper")

json_path: str = "web_scraper/"
cpu_count: int = multiprocessing.cpu_count() * 2
# If file is run locally or tested:
if "tests" in os.getcwd():
    json_path = "web_scraper_tests/"
if "web_scraper" in os.getcwd():
    json_path = ""

# Files where the urls for normal and refused files are stored
url_file = json_helper.JsonHelper(path=f"{json_path}JSON/urls.json")
url_refused_file = json_helper.JsonHelper(path=f"{json_path}JSON/refused_urls.json")

# File where Annex 10 data are stored
annex10_file = json_helper.JsonHelper(path=f"{json_path}JSON/annex10.json")
ema_excel_file = json_helper.JsonHelper(path=f"{json_path}JSON/ema_excel.json")


# Main web scraper function with default settings
def main(config: config_objects.WebConfig):
    """
    Main function that controls which scrapers are activated, and if it runs parallel or not.

    Based on some variables declared at the top of the file, it will scrape the EC website, the EMA website
    and/or downloads the scraped links.

    Args:
        config (config_objects.WebConfig): Object that contains the variables that define the behaviour of webscraper
    """
    medicine_list = config.medicine_list
    if medicine_list is None:
        medicine_list = ec_scraper.scrape_medicines_list()

    log.info(f"=== NEW LOG {datetime.today()} ===")

    Path(f"{json_path}JSON").mkdir(exist_ok=True, parents=True)

    log.info("TASK SUCCESS on Generating directories")

    if config.run_download_annex10:
        url_scraper.get_annex_10_urls("https://www.ema.europa.eu/en/about-us/annual-reports-work-programmes",
                                      annex10_file)

    if config.run_download_ema_excel:
        url_scraper.get_ema_excel_url("https://www.ema.europa.eu/en/medicines/download-medicine-data#european-public-"
                                      "assessment-reports-(epar)-section", ema_excel_file)

    if config.run_scrape_ec:
        ec_scraper.scrape_ec(config, medicine_list, url_file, url_refused_file)

    if config.run_scrape_ema:
        ema_scraper.scrape_ema(config, url_file)

    if config.run_download:
        log.info("TASK START downloading PDF files from fetched urls from EC and EMA")
        download.download_all(config.path_data, url_file, parallel_download=config.parallelized)
        url_file.save_dict()

    if config.run_download_refused:
        log.info("TASK START downloading refused PDF files from fetched urls from EC and EMA")
        download.download_all(config.path_data, url_refused_file, parallel_download=config.parallelized)
        url_refused_file.save_dict()

    if config.run_download_annex10:
        log.info("TASK START downloading Annex 10 Excel files from fetched urls from EC and EMA")
        download.download_annex10_files(config.path_data, annex10_file)

    if ema_excel_file.load_json().get("download_excel", "False") == "True":
        log.info("TASK START downloading EMA excel file from the fetched url")
        print("test")
        # TODO: implement functionality downloading EMA excel file

    if config.run_filter:
        filter_retry.run_filter(3, config.path_data)
    log.info("=== LOG FINISH ===")


# Keep the code locally testable by including this.
# When running this file specifically, the main function will run.
if __name__ == "__main__":
    log_tools.init_loggers()
    main(config_objects.WebConfig().run_custom(scrape_ec=True, scrape_ema=True).set_to_parallel())
