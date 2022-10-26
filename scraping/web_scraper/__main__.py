import json
import logging
from pathlib import Path
from datetime import datetime

from joblib import Parallel, delayed
import tqdm

import download
import ec_scraper
import ema_scraper
import utils
import json_helper

# TODO: These variables are for debugging, remove in final
# Flag variables to indicate whether the webscraper should fill the .csv files or not
scrape_ec: bool = True
scrape_ema: bool = True           # Requires scrape_ec to have been run at least once
download_files: bool = True         # Download pdfs from the obtained links
use_parallelization: bool = True   # Parallelization is currently broken on Windows. Set to False

# list of the type of medicines that will be scraped
# NOTE: This was useful for debugging
scrape_medicine_type: list[ec_scraper.MedicineType] = [
                                                       ec_scraper.MedicineType.HUMAN_USE_ACTIVE,
                                                       # ec_scraper.MedicineType.HUMAN_USE_WITHDRAWN,
                                                       # ec_scraper.MedicineType.ORPHAN_ACTIVE,
                                                       # ec_scraper.MedicineType.ORPHAN_WITHDRAWN
                                                      ]

# TODO: Logging to monolithic main
tqdm_format_string = "{l_bar}{bar}| {n_fmt}/{total_fmt} "

# Global configuration of the log file
log_handler_console = logging.StreamHandler()
log_handler_file = logging.FileHandler("webscraper.log")

logging.basicConfig(level=logging.DEBUG, handlers=[log_handler_console, log_handler_file])

# TODO: To __init__? Figure some stuff out
log = logging.getLogger("webscraper")
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

url_file = json_helper.JsonHelper(path="CSV/urls.json")


# Paralleled function for getting the URL codes. They are written to a CSV file
# TODO: unmarked type for medicine_type
def get_urls_ec(medicine_url: str, eu_n: str, medicine_type: ec_scraper.MedicineType, data_path: str):
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
    pdf_url: dict = {
        eu_n: {
            "epar_url": ema_scraper.pdf_links_from_url(url)
        }
    }
    url_file.add_to_dict(pdf_url)


def main(data_filepath: str = '../../data'):
    log.info(f"=== NEW LOG {datetime.today()} ===")

    Path("CSV").mkdir(exist_ok=True, parents=True)
    # TODO: Remove mkdir filepath after it is moved to monolithic main
    Path(data_filepath).mkdir(exist_ok=True, parents=True)

    log.info("TASK SUCCESS on Generating directories")

    medicine_codes: list[(str, str, int, str)] = ec_scraper.scrape_medicines_list()

    # TODO: Review necessity of JobLib
    with Parallel(n_jobs=12) as parallel:
        # TODO: Progressbar needs to be below logging output
        #       https://stackoverflow.com/questions/6847862/how-to-change-the-format-of-logged-messages-temporarily-in-python
        #       Currently does not work
        # log_handler.setFormatter(logging.Formatter("\r%(message)s"))
        if scrape_ec:
            log.info("TASK START scraping all medicines on the EC website")
            if use_parallelization:
                parallel(
                    delayed(utils.exception_retry(get_urls_ec, logging_instance=log))(medicine_url, eu_n, medicine_type, data_filepath)
                    for (medicine_url, eu_n, medicine_type, _)
                    in tqdm.tqdm(medicine_codes, bar_format=tqdm_format_string)
                )
            else:
                for (medicine_url, eu_n, medicine_type, _) \
                        in tqdm.tqdm(medicine_codes, bar_format=tqdm_format_string):
                    utils.exception_retry(get_urls_ec, logging_instance=log)(medicine_url, eu_n, medicine_type, data_filepath)
            url_file.save_dict()
            log.info("TASK FINISHED EC scrape")

        if scrape_ema:
            log.info("Scraping all individual medicine pages of EMA")
            # Transform JSON object into list of (eu_n, url)
            ema_urls = [(eu_n, url)
                        for eu_n, value_dict in url_file.local_dict.items()
                        for url in value_dict["ema_url"]]

            if use_parallelization:
                parallel(
                    delayed(utils.exception_retry(get_urls_ec, logging_instance=log))(eu_n, urls["ema_url"])
                    for eu_n, urls
                    in tqdm.tqdm(ema_urls, bar_format=tqdm_format_string)
                )
            else:
                for eu_n, url in tqdm.tqdm(ema_urls, bar_format=tqdm_format_string):
                    utils.exception_retry(get_urls_ema, logging_instance=log)(eu_n, url)
            url_file.save_dict()
            log.info("TASK FINISHED EMA scrape")

        # TODO: Same TODO as above
        # log_handler.setFormatter(logging.Formatter("%(message)s"))

    if download_files:
        download.download_all(parallel_download=use_parallelization)


# Keep the code locally testable by including this.
# When running this file specifically, the main function will run.
if __name__ == "__main__":
    main(data_filepath="../../data")
