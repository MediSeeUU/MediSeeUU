import csv
import json
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd
from joblib import Parallel, delayed
import tqdm

from scraping.web_scraper import download
from scraping.web_scraper import ec_scraper
from scraping.web_scraper import ema_scraper
from scraping.web_scraper import utils

# TODO: These variables are for debugging, remove in final
# Flag variables to indicate whether the webscraper should fill the .csv files or not
scrape_ec: bool = False
scrape_ema: bool = False            # Requires scrape_ec to have been run at least once
download_files: bool = True         # Download pdfs from the obtained links
use_parallelization: bool = False   # Parallelization is currently broken on Windows. Set to False

# list of the type of medicines that will be scraped
# NOTE: This was useful for debugging
scrape_medicine_type: list[ec_scraper.MedicineType] = [ec_scraper.MedicineType.HUMAN_USE_ACTIVE,
                                                       ec_scraper.MedicineType.HUMAN_USE_WITHDRAWN,
                                                       ec_scraper.MedicineType.ORPHAN_ACTIVE,
                                                       ec_scraper.MedicineType.ORPHAN_WITHDRAWN]

# TODO: Logging to monolithic main
tqdm_format_string = "{l_bar}{bar}| {n_fmt}/{total_fmt} "

# Global configuration of the log file
log_handler_console = logging.StreamHandler()
log_handler_file = logging.FileHandler("webscraper.log")

logging.basicConfig(level=logging.INFO, handlers=[log_handler_console, log_handler_file])

# TODO: To __init__? Figure some stuff out
# Local instance of a logger
log = logging.getLogger(__name__)


def get_urls_ec(medicine_url: str, eu_n: str, medicine_type: int, data_path: str):
    """ Gets the scraped medicine attributes and urls, and writes them to CSV and JSON files.

    The function writes the data to four (will become three) seperpate CSV files, one for decisions,
    one for annexes, and one for EMA urls. The attributes for the medicine are stored in a single JSON.
    They are all stored in the same data folder, where each medicine gets its own folder.

    Args:
        medicine_url (str): url to a medicine page for a specific medicine.
        eu_n (str): EU number of the medicine.
        medicine_type (int): The type of medicine.
        data_path (str): The path where the CSV and JSON files need to be stored.

    Returns:
        None: This function returns nothing.
    """
    if ec_scraper.MedicineType(medicine_type) in scrape_medicine_type:
        # getURLsForPDFAndEMA returns per medicine the urls
        # for the decision and annexes files and for the ema website.
        dec_list, anx_list, ema_list, attributes_dict = \
            ec_scraper.scrape_medicine_page(medicine_url, ec_scraper.MedicineType(medicine_type))

        with open("web_scraper/CSV/decision.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([eu_n, dec_list])

        with open("web_scraper/CSV/annexes.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([eu_n, anx_list])

        with open("web_scraper/CSV/ema_urls.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([eu_n, ema_list])

        with open("web_scraper/CSV/med_dict.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([eu_n, attributes_dict])

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

    Returns:
        None: This function returns nothing
    """
    if url != "[]":
        url = json.loads(url.replace('\'', '"'))[0]
    else:
        url = ''

    pdf_url = ema_scraper.pdf_links_from_url(url)

    with open("web_scraper/CSV/epar.csv", 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([eu_n, pdf_url])


def main(data_filepath='../data'):
    """ Main function that controls which scrapers are activated, and if it runs parallel or not.

    Based on some variables declared at the top of the file, it will scrape the EC website, the EMA website
    and/or downloads the scraped links.

    Args:
        data_filepath (str, optional): The file path where all data needs to be stored. Defaults to '../data'.

    Returns:
        None: This function returns nothing.
    """
    log.info(f"=== NEW LOG {datetime.today()} ===")

    # TODO: Remove mkdir after it is moved to monolithic main
    # Create the data dir.
    # The ' exist_ok' option ensures no errors thrown if this is not the first time the code runs.
    Path("web_scraper/CSV").mkdir(exist_ok=True, parents=True)
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
                    delayed(get_urls_ec)(medicine_url, eu_n, medicine_type, data_filepath)
                    for (medicine_url, eu_n, medicine_type, _)
                    in tqdm.tqdm(medicine_codes, bar_format=tqdm_format_string)
                )
            else:
                for (medicine_url, eu_n, medicine_type, _) \
                        in tqdm.tqdm(medicine_codes, bar_format=tqdm_format_string):
                    get_urls_ec(medicine_url, eu_n, medicine_type, data_filepath)
            log.info("TASK FINISHED EC scrape")

    if scrape_ema:
        log.info("Scraping all individual medicine pages of EMA")
        ema = pd.read_csv('web_scraper/CSV/ema_urls.csv', header=None, index_col=0, on_bad_lines='skip').squeeze().to_dict()
        if use_parallelization:
            parallel(
                delayed(get_urls_ema)(url[0], url[1])
                for url
                in tqdm.tqdm(ema.items(), bar_format=tqdm_format_string)
            )
        else:
            for url in tqdm.tqdm(ema.items(), bar_format=tqdm_format_string):
                utils.exception_retry(get_urls_ema(url[0], url[1]))
        log.info("TASK FINISHED EMA scrape")

        # TODO: Same TODO as above
        # log_handler.setFormatter(logging.Formatter("%(message)s"))

    if download_files:
        download.download_all(parallel_download=use_parallelization)


# Keep the code locally testable by including this.
# When running this file specifically, the main function will run.
if __name__ == "__main__":
    main()
