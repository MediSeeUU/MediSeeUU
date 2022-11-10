import json
import logging
from pathlib import Path
from datetime import datetime
import os

import tqdm
import tqdm.contrib.concurrent as tqdm_concurrent
import tqdm.contrib.logging as tqdm_logging

from scraping.web_scraper import download, ec_scraper, ema_scraper, utils, json_helper, filter_retry


# TODO: These variables are for debugging, remove in final
# Flag variables to indicate whether the webscraper should fill the .csv files or not
scrape_ec: bool = True
scrape_ema: bool = False            # Requires scrape_ec to have been run at least once
scrape_annex10: bool = False
download_files: bool = False         # Download pdfs from the obtained links
run_filter: bool = False
use_parallelization: bool = True   # Parallelization is currently broken on Windows. Set to False

# list of the type of medicines that will be scraped
# NOTE: This was useful for debugging
scrape_medicine_type: list[ec_scraper.MedicineType] = [
                                                       ec_scraper.MedicineType.HUMAN_USE_ACTIVE,
                                                       ec_scraper.MedicineType.HUMAN_USE_WITHDRAWN,
                                                       ec_scraper.MedicineType.ORPHAN_ACTIVE,
                                                       ec_scraper.MedicineType.ORPHAN_WITHDRAWN
                                                      ]

# TODO: Logging to monolithic main
tqdm_format_string = "{l_bar}{bar}| {n_fmt}/{total_fmt} "

# Global configuration of the log file
log_handler_console = logging.StreamHandler()
log_handler_file = logging.FileHandler("webscraper.log")

logging.basicConfig(level=logging.INFO, handlers=[log_handler_console, log_handler_file])

# TODO: To __init__? Figure some stuff out
log = logging.getLogger("webscraper")
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

json_path = "web_scraper/"
# If file is run locally:
if "web_scraper" in os.getcwd():
    json_path = ""
url_file = json_helper.JsonHelper(path=f"{json_path}JSON/urls.json")
annex10_file = json_helper.JsonHelper(path=f"{json_path}JSON/annex10.json")


# Paralleled function for getting the URL codes. They are written to a JSON file
# TODO: unmarked type for medicine_type
def get_urls_ec(medicine_url: str, eu_n: str, medicine_type: ec_scraper.MedicineType, data_path: str):
    """ Gets the scraped medicine attributes and urls, and writes them to CSV and JSON files.

    The function writes the data to four (will become three) separate CSV files, one for decisions,
    one for annexes, and one for EMA urls. The attributes for the medicine are stored in a single JSON.
    They are all stored in the same data folder, where each medicine gets its own folder.

    Args:
        medicine_url (str): url to a medicine page for a specific medicine.
        eu_n (str): EU number of the medicine.
        medicine_type (int): The type of medicine.
        data_path (str): The path where the CSV and JSON files need to be stored.
    """
    # A list of the medicine types we want to scrape is defined in this file
    # If the entered medicine_type is not in that list, this method will ignore
    if ec_scraper.MedicineType(medicine_type) not in scrape_medicine_type:
        return

    # dec_ anx_ and ema_list are lists of URLs to PDF files
    # Attributes_dict is a dictionary containing the attributes scraped from the EC page
    dec_list, anx_list, ema_list, attributes_dict = \
        ec_scraper.scrape_medicine_page(medicine_url, ec_scraper.MedicineType(medicine_type))

    # TODO: Common name structure?
    url_json: dict[str, list[str]] = {
        eu_n: {
            "ec_url": medicine_url,
            "aut_url": dec_list,
            "smpc_url": anx_list,
            "ema_url": ema_list
        }
    }

    url_file.add_to_dict(url_json)

    # Creates a directory if the medicine doesn't exist yet,
    # otherwise it just adds the json file to the existing directory
    Path(f"{data_path}/{eu_n}").mkdir(exist_ok=True)
    with open(f"{data_path}/{eu_n}/{eu_n}_attributes.json", 'w') as f:
        json.dump(attributes_dict, f, indent=4)


def get_urls_ema(eu_n: str, url: str):
    """ Gets all the pdf urls from the EMA website and writes it to a CSV file.

        Args:
            eu_n (str): The EU number of the medicine.
            url (str): The url to an EMA page for a specific medicine.
        """
    epar_url, omar_url = ema_scraper.pdf_links_from_url(url)

    pdf_url: dict[str, str] = {
        eu_n: {
            "epar_url": epar_url,
            "omar_url": omar_url
        }
    }
    url_file.add_to_dict(pdf_url)


def get_excel_ema(url: str):
    """ Gets all annex10 files from the EMA website

    Args:
        url (str): link to where all annex10 files are stored
    """

    excel_url: dict[str, dict[str, str]] = ema_scraper.get_annex10_files(url, annex10_file.load_json())
    annex10_file.overwrite_dict(excel_url)


def main(data_filepath: str = '../data'):
    """ Main function that controls which scrapers are activated, and if it runs parallel or not.

        Based on some variables declared at the top of the file, it will scrape the EC website, the EMA website
        and/or downloads the scraped links.

        Args:
            data_filepath (str, optional): The file path where all data needs to be stored. Defaults to '../data'.
        """
    log.info(f"=== NEW LOG {datetime.today()} ===")

    Path(f"{json_path}JSON").mkdir(exist_ok=True, parents=True)
    # TODO: Remove mkdir filepath after it is moved to monolithic main
    # Path(data_filepath).mkdir(exist_ok=True, parents=True)

    log.info("TASK SUCCESS on Generating directories")

    medicine_codes: list[(str, str, int, str)] = ec_scraper.scrape_medicines_list()

    if scrape_annex10:
        log.info("TASK START scraping all annex10 files on the EMA website")

        get_excel_ema("https://www.ema.europa.eu/en/about-us/annual-reports-work-programmes")

        annex10_file.save_dict()

        log.info("TASK FINISHED annex10 scrape")

    if scrape_ec:
        log.info("TASK START scraping all medicines on the EC website")

        get_urls_ec_retry = utils.exception_retry(get_urls_ec, logging_instance=log)

        # Transform zipped list into individual lists for thread_map function
        # The last element of the medicine_codes tuple is not of interest, thus we pop()

        with tqdm_logging.logging_redirect_tqdm():
            if use_parallelization:
                unzipped_medicine_codes = [list(t) for t in zip(*medicine_codes)]
                unzipped_medicine_codes.pop()
                tqdm_concurrent.thread_map(get_urls_ec_retry,
                                           *unzipped_medicine_codes,
                                           [data_filepath] * len(medicine_codes), max_workers=24)
            else:
                for (medicine_url, eu_n, medicine_type, _) in tqdm.tqdm(medicine_codes):
                    get_urls_ec_retry(medicine_url, eu_n, medicine_type, data_filepath)

        url_file.save_dict()
        log.info("TASK FINISHED EC scrape")

    if scrape_ema:
        log.info("Scraping all individual medicine pages of EMA")

        if not scrape_ec:
            url_file.load_json()

        get_urls_ema_retry: callable = utils.exception_retry(get_urls_ema, logging_instance=log)

        # Transform JSON object into list of (eu_n, url)
        ema_urls = [(eu_n, url)
                    for eu_n, value_dict in url_file.local_dict.items()
                    for url in value_dict["ema_url"]]

        unzipped_ema_urls = [list(t) for t in zip(*ema_urls)]

        with tqdm_logging.logging_redirect_tqdm():
            if use_parallelization:
                tqdm_concurrent.thread_map(get_urls_ema_retry, *unzipped_ema_urls, max_workers=24)

            else:
                for eu_n, url in tqdm.tqdm(ema_urls, bar_format=tqdm_format_string):
                    get_urls_ema_retry(eu_n, url)

        url_file.save_dict()
        log.info("TASK FINISHED EMA scrape")

    if download_files:
        log.info("TASK START downloading PDF files from fetched urls from EC and EMA")

        download.download_all(data_filepath, url_file, parallel_download=use_parallelization)

        log.info("TASK FINISHED downloading PDF files")

    if run_filter:
        filter_retry.run_filter(3, data_filepath)
    log.info("=== LOG FINISH ===")


# Keep the code locally testable by including this.
# When running this file specifically, the main function will run.
if __name__ == "__main__":
    main(data_filepath="../../data")
