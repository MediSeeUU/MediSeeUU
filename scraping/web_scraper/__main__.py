import logging
import multiprocessing
from datetime import datetime
from pathlib import Path

import scraping.utilities.log.log_tools as log_tools
import scraping.utilities.web.config_objects as config_objects
from scraping.utilities.web import json_helper
from scraping.web_scraper import download, ec_scraper, ema_scraper, filter_retry
from scraping.web_scraper import url_scraper

log = logging.getLogger("web_scraper")

cpu_count: int = multiprocessing.cpu_count() * 2

# We want to save the JSON in the same location through different runs
# This code makes sure it is always the same location
# TODO: Specify in some config file?
match Path.cwd().name:
    case "tests":                                   # Running as a test
        json_path_prefix = "web_scraper_tests/"
    case "web_scraper":                             # Running from the web_scraper module instead of global main
        json_path_prefix = ""
    case _:                                         # Running from global main
        json_path_prefix = "web_scraper/"

json_path = json_path_prefix + "JSON/"


url_file = json_helper.JsonHelper(json_path + "urls.json")
url_refused_file = json_helper.JsonHelper(json_path + "refused_urls.json")
annex10_file = json_helper.JsonHelper(json_path + "annex10.json")


# Main web scraper function with default settings
def main(config: config_objects.WebConfig):
    """
    Main function that controls which scrapers are activated, and if it runs parallel or not.

    Based on some variables declared at the top of the file, it will scrape the EC website, the EMA website
    and/or downloads the scraped links.

    Args:
        config (config_objects.WebConfig): Object that contains the variables that define the behaviour of webscraper
    """
    log.info(f"=== NEW LOG {datetime.today()} ===")

    medicine_list = config.medicine_list
    if medicine_list is None:
        medicine_list = ec_scraper.scrape_medicines_list()

    Path(json_path).mkdir(exist_ok=True, parents=True)

    log.info("TASK SUCCESS on Generating directories")

    if config.run_download_annex10:
        url_scraper.get_annex_10_urls("https://www.ema.europa.eu/en/about-us/annual-reports-work-programmes",
                                      annex10_file)

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

    if config.run_download_ema_excel:
        if ema_scraper.get_epar_excel_url("https://www.ema.europa.eu/en/medicines/download-medicine-data#european-"
                                          "public-assessment-reports-(epar)-section", ema_excel_file):
            log.info("TASK START downloading EMA excel file from the fetched url")
            download.download_ema_excel_file(config.path_data, ema_excel_file)

    if config.run_filter:
        filter_retry.run_filter(3, config.path_data)
    log.info("=== LOG FINISH ===")


# Keep the code locally testable by including this.
# When running this file specifically, the main function will run.
if __name__ == "__main__":
    log_tools.init_loggers()
    main(config_objects.WebConfig().run_custom(scrape_ec=True, scrape_ema=True).set_to_parallel())
