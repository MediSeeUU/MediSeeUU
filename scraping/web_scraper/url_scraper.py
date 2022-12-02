import logging
from scraping.web_scraper import ema_scraper, ec_scraper, save_webdata
from scraping.utilities.web import web_utils as utils, json_helper, config_objects
from scraping.utilities.web.medicine_type import MedicineType
import scraping.utilities.definitions.attributes as attr
from datetime import datetime

log = logging.getLogger("web_scraper")


# list of the type of medicines that will be scraped
scrape_medicine_type: list[MedicineType] = [
    MedicineType.HUMAN_USE_ACTIVE,
    MedicineType.HUMAN_USE_WITHDRAWN,
    MedicineType.ORPHAN_ACTIVE,
    MedicineType.ORPHAN_WITHDRAWN,
    MedicineType.HUMAN_USE_REFUSED,
    MedicineType.ORPHAN_REFUSED
]


def get_annex_10_urls(url: str, annex_dict: json_helper.JsonHelper):
    """
    Gets all annex10 files from the EMA website

    Args:
        url (str): link to where all annex10 files are stored
        annex_dict (dict[int, dict[str, str]]): Dictionary that contains links to the annex files per year
            and when they were last updated
    """
    log.info("TASK START scraping all annex10 URLs from the EMA website")
    excel_url: dict[str, dict[str, str]] = ema_scraper.get_annex10_data(url, annex_dict.load_json())
    annex_dict.overwrite_dict(excel_url)
    annex_dict.save_dict()
    log.info("TASK FINISHED annex10 scrape")


# Paralleled function for getting the URL codes. They are written to a JSON file
# TODO: unmarked type for medicine_type
@utils.exception_retry(logging_instance=log)
def get_urls_ec(medicine_url: str, eu_n: str, medicine_type: MedicineType, data_path: str,
                url_file: json_helper.JsonHelper, url_refused_file: json_helper.JsonHelper):
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
        url_file (json_helper.JsonHelper): the dictionary containing all the urls of a specific medicine
        url_refused_file (json_helper.JsonHelper): the dictionary containing all the urls of a specific medicine
    """
    # A list of the medicine types we want to scrape is defined in this file
    # If the entered medicine_type is not in that list, this method will ignoreW
    if MedicineType(medicine_type) not in scrape_medicine_type:
        return

    # Retrieves the date the EC medicine page was last updated
    html_active = utils.get_html_object(medicine_url)
    medicine_last_updated_date = ec_scraper.get_last_updated_date(html_active)

    # Checks whether attributes and files need to be scraped from the EC web page
    if not check_scrape_page(eu_n, medicine_last_updated_date, "ec", url_file):
        return

    # dec_ anx_ and ema_list are lists of URLs to PDF files
    # Attributes_dict is a dictionary containing the attributes scraped from the EC page
    dec_list_indexed, anx_list_indexed, ema_list, attributes_dict = \
        ec_scraper.scrape_medicine_page(eu_n, html_active, medicine_type, data_path)

    # Sort decisions and annexes list
    dec_list_indexed.sort(key=lambda x: int(x[1]))
    anx_list_indexed.sort(key=lambda x: int(x[1]))

    # Lift url out of tuple and ignore index. [(str, int)] -> [str]
    dec_list = [x[0] for x in dec_list_indexed]
    anx_list = [x[0] for x in anx_list_indexed]

    # if initial is addressed to member states, move first url to end of url list
    if attributes_dict[attr.init_addressed_to_member_states] == "True":
        dec_list.append(dec_list.pop(0))
        anx_list.append(anx_list.pop(0))

    save_webdata.set_active_refused_webdata(eu_n, medicine_url, dec_list, anx_list, ema_list, attributes_dict,
                                            data_path, url_file, url_refused_file)


@utils.exception_retry(logging_instance=log)
def get_urls_ema(eu_n: str, url: str, url_file: json_helper.JsonHelper):
    """
    Gets all the pdf urls from the EMA website and writes it to a file.

    Args:
        eu_n (str): The EU number of the medicine.
        url (str): The url to an EMA page for a specific medicine.
        url_file (json_helper.JsonHelper): the dictionary containing all the urls of a specific medicine
    """
    # Retrieves the date the EMA medicine page was last updated
    html_active = utils.get_html_object(url)
    medicine_last_updated_date: datetime = ema_scraper.find_last_updated_date(html_active)

    # Checks whether attributes and files need to be scraped from the EMA web page
    if not check_scrape_page(eu_n, medicine_last_updated_date, "ema", url_file):
        return

    ema_urls: dict[str, str | list[tuple]] = ema_scraper.scrape_medicine_page(url, html_active)

    pdf_url: dict[str, dict] = {
        eu_n: ema_urls
    }

    url_file.add_to_dict(pdf_url)


def check_scrape_page(eu_n: str, medicine_last_updated: datetime, last_scraped_type: str,
                      url_file: json_helper.JsonHelper) -> bool:
    """
    Checks whether the medicine page (either EC or EMA) has been updated since last scrape cycle, or that the page has
    never been scraped at all. Based on this it returns a boolean that indicates whether attributes and files need to be
    fetched from the html

    Args:
        eu_n (str): EU number of the medicine
        medicine_last_updated (datetime): Date since the page was last updated
        last_scraped_type (str): The page type (either EC or EMA)
        url_file (json_helper.JsonHelper): the dictionary containing all the urls of a specific medicine

    Returns:
        bool: False indicates that the website has not been updated since the last scrape cycle
    """
    # Logic to decide whether this function should search for new files and attributes for a medicine
    try:
        # If the last medicine updated date is later than the date of the last scrape cycle, the url.json should be
        # updated
        if medicine_last_updated.date() > datetime.strptime(url_file.local_dict[eu_n]
                                                            [f"{last_scraped_type}_last_scraped"], '%d/%m/%Y').date():
            log.info(f"{eu_n}: {last_scraped_type.upper()} page has been updated since last scrape cycle")
            return True
        # Otherwise, it returns this function, since there are no new files or attributes
        else:
            return False
    except KeyError:
        # Whenever above function can't find the EU number in the JSON, or the last scraped date for the EC, then it
        # should also update urls.json
        return True
