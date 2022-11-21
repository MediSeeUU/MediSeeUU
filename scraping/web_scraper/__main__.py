import json
from pathlib import Path
from datetime import datetime
import os
import multiprocessing
import logging

import tqdm
import tqdm.contrib.concurrent as tqdm_concurrent
import tqdm.contrib.logging as tqdm_logging

from scraping.web_scraper import download, ec_scraper, ema_scraper, utils, json_helper, filter_retry

# list of the type of medicines that will be scraped
scrape_medicine_type: list[ec_scraper.MedicineType] = [
    ec_scraper.MedicineType.HUMAN_USE_ACTIVE,
    ec_scraper.MedicineType.HUMAN_USE_WITHDRAWN,
    ec_scraper.MedicineType.ORPHAN_ACTIVE,
    ec_scraper.MedicineType.ORPHAN_WITHDRAWN,
    ec_scraper.MedicineType.HUMAN_USE_REFUSED,
    ec_scraper.MedicineType.ORPHAN_REFUSED
]

log = logging.getLogger("web_scraper")

json_path: str = "web_scraper/"
cpu_count: int = multiprocessing.cpu_count() * 2
# If file is run locally:
if "web_scraper" in os.getcwd():
    json_path = ""


# Files where the urls for normal and refused files are stored
url_file = json_helper.JsonHelper(path=f"{json_path}JSON/urls.json")
url_refused_file = json_helper.JsonHelper(path=f"{json_path}JSON/refused_urls.json")

scrape_annex10: bool = False
# File where Annex 10 data are stored
annex10_file = json_helper.JsonHelper(path=f"{json_path}JSON/annex10.json")


def check_scrape_page(eu_n: str, medicine_last_updated_date: datetime, last_scraped_type: str) -> bool:
    """
    Checks whether the medicine page (either EC or EMA) has been updated since last scrape cycle, or that the page has
    never been scraped at all. Based on this it returns a boolean that indicates whether attributes and files need to be
    fetched from the html

    Args:
        eu_n (str): EU number of the medicine
        medicine_last_updated_date (datetime): Date since the page was last updated
        last_scraped_type (str): The page type (either EC or EMA)

    Returns:
        bool: False indicates that the website has not been updated since the last scrape cycle
    """
    # Logic to decide whether this function should search for new files and attributes for a medicine
    try:
        # If the last medicine updated date is later than the date of the last scrape cycle, the url.json should be
        # updated
        if medicine_last_updated_date.date() > datetime.strptime(url_file.local_dict[eu_n][last_scraped_type],
                                                                 '%d/%m/%Y').date():
            return True
        # Otherwise, it returns this function, since there are no new files or attributes
        else:
            return False
    except KeyError:
        # Whenever above function can't find the EU number in the JSON, or the last scraped date for the EC, then it
        # should also update urls.json
        return True


# Paralleled function for getting the URL codes. They are written to a JSON file
# TODO: unmarked type for medicine_type
@utils.exception_retry(logging_instance=log)
def get_urls_ec(medicine_url: str, eu_n: str, medicine_type: ec_scraper.MedicineType, data_path: str):
    """
    Gets the scraped medicine attributes and urls, and writes them to CSV and JSON files.

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

    # Retrieves the date the EC medicine page was last updated
    html_active = utils.get_html_object(medicine_url)
    medicine_last_updated_date = ec_scraper.get_last_updated_date(html_active)

    # Checks whether attributes and files need to be scraped from the EC web page
    if not check_scrape_page(eu_n, medicine_last_updated_date, "ec_last_scraped"):
        return

    log.info(eu_n + ": EC page has been updated since last scrape cycle")

    # dec_ anx_ and ema_list are lists of URLs to PDF files
    # Attributes_dict is a dictionary containing the attributes scraped from the EC page
    dec_list_indexed, anx_list_indexed, ema_list, attributes_dict = \
        ec_scraper.scrape_medicine_page(medicine_url, html_active, ec_scraper.MedicineType(medicine_type))

    # Sort decisions and annexes list
    dec_list_indexed.sort(key=lambda x: int(x[1]))
    anx_list_indexed.sort(key=lambda x: int(x[1]))

    # Lift url out of tuple and ignore index. [(str, int)] -> [str]
    dec_list = [x[0] for x in dec_list_indexed]
    anx_list = [x[0] for x in anx_list_indexed]

    # if initial is addressed to member states, move first url to end of url list
    if attributes_dict["init_addressed_to_member_states"] == "True":
        dec_list.append(dec_list.pop(0))
        anx_list.append(anx_list.pop(0))

    set_active_refused_save_parameters(eu_n, medicine_url, dec_list, anx_list, ema_list, attributes_dict, data_path)


def set_active_refused_save_parameters(eu_n: str, medicine_url: str, dec_list: list[str], anx_list: list[str],
                                       ema_list: list[str], attributes_dict: dict[str, str], data_path: str):
    """
    Based on whether the medicine is refused or not, it will set the parameters, so that it can be saved to the file
    system correctly.

    Args:
        eu_n (str): EU number of the medicine.
        medicine_url (str): url to a medicine page for a specific medicine.
        dec_list (list[str]): List of urls to decisions on the EC website.
        anx_list (list[str]): List of urls to annexes on the EC website.
        ema_list (list[str]): List of urls to EMA pages on the EC website.
        attributes_dict (dict[str, str]): Dictionary of scraped attributes on the EC website
        data_path (str): The path where the JSON files need to be stored.
    """
    # Sets parameter values for active and withdrawn medicines that need to be saved
    if attributes_dict["eu_aut_status"] != "REFUSED":
        medicine_identifier: str = eu_n
        target_path: str = f"{data_path}/{medicine_identifier}"
        save_medicine_urls_and_attributes(medicine_identifier, medicine_url, dec_list, anx_list, ema_list,
                                          attributes_dict, url_file, target_path)
    # Sets parameter values for refused medicines that need to be saved
    else:
        # Checks if the medicine is a human or orphan one, and based on that picks the right EMA number
        if attributes_dict["orphan_status"] == "h":
            ema_number: str = "ema_number"
        else:
            ema_number: str = "ema_od_number"

        # Based on whether there is an EMA number, sets the medicine identifier to the EMA number or the product name
        if attributes_dict[ema_number] != "":
            medicine_identifier: str = "REFUSED-" + attributes_dict[ema_number].replace('/', '-')
        else:
            medicine_identifier: str = "REFUSED-" + attributes_dict["eu_brand_name_current"].replace('/', '-')

        target_path: str = f"{data_path}/refused/{medicine_identifier}"
        save_medicine_urls_and_attributes(medicine_identifier, medicine_url, dec_list, anx_list, ema_list,
                                          attributes_dict, url_refused_file, target_path)


def save_medicine_urls_and_attributes(medicine_identifier: str, medicine_url: str, dec_list: list[str],
                                      anx_list: list[str], ema_list: list[str], attributes_dict: dict[str, str],
                                      file: json_helper.JsonHelper, target_path: str):
    """
    Saves a JSON file in the correct location, containing scraped attributes from the EC website. It also adds urls to
    the right url JSON files.

    Args:
        medicine_identifier (str): Identifier for a medicine. An EU number for non-refused medicine, EMA number for
            refused medicine
        medicine_url (str): url to a medicine page for a specific medicine.
        dec_list (list[str]): List of urls to decisions on the EC website.
        anx_list (list[str]): List of urls to annexes on the EC website.
        ema_list (list[str]): List of urls to EMA pages on the EC website.
        attributes_dict (dict[str, str]): Dictionary of scraped attributes on the EC website
        file (json_helper.JsonHelper): The url json where all the data needs to be stored.
        target_path (str): Directory where the json needs to be stored.
    """
    # TODO: Common name structure?
    url_json: dict[str, list[str]] = {
        medicine_identifier: {
            "ec_url": medicine_url,
            "aut_url": dec_list,
            "smpc_url": anx_list,
            "ema_url": ema_list,
            "ec_last_scraped": datetime.strftime(datetime.today(), '%d/%m/%Y'),
            "overwrite_ec_files": "True"
        }
    }

    file.add_to_dict(url_json)

    # Creates a directory if the medicine doesn't exist yet,
    # otherwise it just adds the json file to the existing directory
    Path(f"{target_path}").mkdir(exist_ok=True)
    with open(f"{target_path}/{medicine_identifier}_webdata.json", 'w') as f:
        json.dump(attributes_dict, f, indent=4)


@utils.exception_retry(logging_instance=log)
def get_urls_ema(eu_n: str, url: str):
    """
    Gets all the pdf urls from the EMA website and writes it to a file.

    Args:
        eu_n (str): The EU number of the medicine.
        url (str): The url to an EMA page for a specific medicine.
    """

    # Retrieves the date the EMA medicine page was last updated
    html_active = utils.get_html_object(url)
    medicine_last_updated_date: datetime = ema_scraper.find_last_updated_date(html_active)

    # Checks whether attributes and files need to be scraped from the EMA web page
    if not check_scrape_page(eu_n, medicine_last_updated_date, "ema_last_scraped"):
        return

    log.info(eu_n + ": EMA page has been updated since last scrape cycle")

    ema_urls: dict[str, str | list[str]] = ema_scraper.scrape_medicine_page(url, html_active)

    pdf_url: dict[str, dict] = {
        eu_n: ema_urls
    }

    url_file.add_to_dict(pdf_url)


def get_excel_ema(url: str):
    """
    Gets all annex10 files from the EMA website

    Args:
        url (str): link to where all annex10 files are stored
    """
    excel_url: dict[str, dict[str, str]] = ema_scraper.get_annex10_files(url, annex10_file.load_json())
    annex10_file.overwrite_dict(excel_url)


# Main web scraper function with default settings
def main(data_filepath: str = "../data",
         scrape_ec: bool = True, scrape_ema: bool = True, download_files: bool = True,
         download_refused_files: bool = True, run_filter: bool = True, use_parallelization: bool = True,
         medicine_list: (list[(str, str, int, str)]) | None = None):
    """
    Main function that controls which scrapers are activated, and if it runs parallel or not.

    Based on some variables declared at the top of the file, it will scrape the EC website, the EMA website
    and/or downloads the scraped links.

    Args:
        data_filepath (str, optional): The file path where all data needs to be stored. Defaults to "../data".
        scrape_ec (bool): Whether EC URLs should be scraped
        scrape_ema (bool): Whether EMA URLs should be scraped | Requires scrape_ec to have been run at least once
        download_files (bool): Whether scraper should download PDFs from obtained links
        download_refused_files (bool): Whether scraper should download refused PDFs from obtained links
        run_filter (bool): Whether filter should be run after downloading PDF files
        use_parallelization (bool): Whether downloading should be parallel (faster)
        medicine_list (list[(str, str, int, str)] | None): List of medicine elements
    """
    if medicine_list is None:
        medicine_list = ec_scraper.scrape_medicines_list()

    log.info(f"=== NEW LOG {datetime.today()} ===")

    Path(f"{json_path}JSON").mkdir(exist_ok=True, parents=True)

    log.info("TASK SUCCESS on Generating directories")

    if scrape_annex10:
        log.info("TASK START scraping all annex10 files on the EMA website")

        get_excel_ema("https://www.ema.europa.eu/en/about-us/annual-reports-work-programmes")

        annex10_file.save_dict()

        log.info("TASK FINISHED annex10 scrape")

    if scrape_ec:
        with open("no_english_available.txt", 'w', encoding="utf-8") as f:
            pass  # open/clean no_english_available file
        # make sure tests start with empty dict, because url_file is global variable only way to do this is here.
        if "test" in os.getcwd():
            url_file.overwrite_dict({})
        log.info("TASK START scraping all medicines on the EC website")
        # Transform zipped list into individual lists for thread_map function
        # The last element of the medicine_codes tuple is not of interest, thus we pop()

        with tqdm_logging.logging_redirect_tqdm():
            if use_parallelization:
                unzipped_medicine_list = [list(t) for t in zip(*medicine_list)]
                unzipped_medicine_list.pop()
                tqdm_concurrent.thread_map(get_urls_ec,
                                           *unzipped_medicine_list,
                                           [data_filepath] * len(medicine_list), max_workers=cpu_count)
            else:
                for (medicine_url, eu_n, medicine_type, _) in tqdm.tqdm(medicine_list):
                    get_urls_ec(medicine_url, eu_n, medicine_type, data_filepath)

        url_file.save_dict()
        url_refused_file.save_dict()

        log.info("TASK FINISHED EC scrape")

    if scrape_ema:
        log.info("Scraping all individual medicine pages of EMA")

        if not scrape_ec:
            url_file.load_json()

        # Transform JSON object into list of (eu_n, url)
        ema_urls: list[tuple[str, str]] = [
            (eu_n, url)
            for eu_n, value_dict in url_file.local_dict.items()
            for url in value_dict["ema_url"]
        ]

        unzipped_ema_urls: list[list[str]] = [list(t) for t in zip(*ema_urls)]

        with tqdm_logging.logging_redirect_tqdm():
            if use_parallelization and len(unzipped_ema_urls) > 0:
                tqdm_concurrent.thread_map(get_urls_ema, *unzipped_ema_urls, max_workers=cpu_count)

            else:
                for eu_n, url in tqdm.tqdm(ema_urls):
                    get_urls_ema(eu_n, url)

        url_file.save_dict()
        log.info("TASK FINISHED EMA scrape")

    if download_files:
        log.info("TASK START downloading PDF files from fetched urls from EC and EMA")

        download.download_all(data_filepath, url_file, parallel_download=use_parallelization)
        download.save_new_eu_numbers(data_filepath)

        url_file.save_dict()
        log.info("TASK FINISHED downloading PDF files")

    if download_refused_files:
        log.info("TASK START downloading refused PDF files from fetched urls from EC and EMA")

        download.download_all(data_filepath, url_refused_file, parallel_download=use_parallelization)

        url_refused_file.save_dict()
        log.info("TASK FINISHED downloading refused PDF files")

    if run_filter:
        filter_retry.run_filter(3, data_filepath)
    log.info("=== LOG FINISH ===")


# Keep the code locally testable by including this.
# When running this file specifically, the main function will run.
if __name__ == "__main__":
    import scraping.log_setup
    scraping.log_setup.init_loggers()

    main(data_filepath="../../data")
