import json
import logging
import multiprocessing
import os
from datetime import date, datetime, timedelta
from itertools import repeat

import bs4
import regex as re
import requests
import tqdm.contrib.concurrent as tqdm_concurrent
import tqdm.contrib.logging as tqdm_logging
from tqdm import tqdm

import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.values as values
import scraping.utilities.log.log_tools as log_tools
from scraping.utilities.web import web_utils as utils, config_objects, json_helper
from scraping.utilities.web.medicine_type import MedicineType
from scraping.web_scraper import url_scraper

log = logging.getLogger("web_scraper.ec_scraper")
cpu_count: int = multiprocessing.cpu_count() * 2


# links to the ec pages that contain medicine codes
HUMAN_USE_ACTIVE_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_hum_act.htm?sort=a"
HUMAN_USE_WITHDRAWN_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_hum_nact.htm?sort=a"
HUMAN_USE_REFUSED_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_hum_refus.htm"
ORPHAN_ACTIVE_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_od_act.htm?sort=a"
ORPHAN_WITHDRAWN_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_od_nact.htm?sort=a"
ORPHAN_REFUSED_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_od_refus.htm"


def scrape_medicines_list() -> list[(str, str, int, str)]:
    """
    Scrape the EC website, and construct urls to all individual medicine pages.

    From the EC website, the JSON files for active and withdrawn medicine are scraped. The JSONs
    contain information about the medicine that is needed to construct a link to each individual medicine page.
    It does so for all active and withdrawn, orphan and human use medicine.

    Returns:
        list[(str, str, int, str)]:
            The links to the medicine pages are stored in a list, along with the full EU number,
            the medicine type and a short EU number.

    """
    medicine_list: list[(str, str, int, str)] = []

    # Loops over all the JSON objects that contain the short eu numbers, so that they can be stored
    # The first JSON object is for active human use medicine, the second for withdrawn human use,
    # the third for active orphan and the fourth for withdrawn orphan
    # This corresponds with the indices of the MedicineType enum
    medicine_type: int = 0
    for parsed_json in scrape_active_withdrawn_jsons():
        # Each row has an object eu_num: { display, pre, id }
        # The URL on the EC website uses the pre and id
        for row in parsed_json:
            eu_num_short: str = row['eu_num']['pre'] + row['eu_num']['id']
            eu_num_full: str = (row['eu_num']['display']).replace("/", "-")

            ec_link = f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm"
            medicine_list.append((ec_link, eu_num_full, medicine_type, eu_num_short))
        medicine_type += 1

    for parsed_json in scrape_refused_jsons():
        for row in parsed_json:
            eu_num_short: str = row['name']['pre'] + str(row['name']['id'])
            eu_num_full: str = "REFUSED-" + row['name']['display']

            ec_link = f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm"
            medicine_list.append((ec_link, eu_num_full, medicine_type, eu_num_short))
        medicine_type += 1

    return medicine_list


def scrape_active_withdrawn_jsons() -> list[dict]:
    """
    Scrape the EC website for active and withdrawn medicine JSONs.

    The JSON files that are scraped are needed to construct the url to each individual medicine page.

    Returns:
        list[dict]: The list of JSONs that for active and withdrawn, human use and orphan medicine.
    """
    active_withdrawn_json_list: list[dict] = [get_ec_json_objects(get_ec_html(HUMAN_USE_ACTIVE_URL))[0],
                                              get_ec_json_objects(get_ec_html(HUMAN_USE_WITHDRAWN_URL))[0],
                                              get_ec_json_objects(get_ec_html(ORPHAN_ACTIVE_URL))[0],
                                              get_ec_json_objects(get_ec_html(ORPHAN_WITHDRAWN_URL))[0]]
    return active_withdrawn_json_list


def scrape_refused_jsons() -> list[dict]:
    """
    Scrape the EC website for refused medicine JSONs.

    The JSON files that are scraped are needed to construct the url to each individual medicine page.

    Returns:
        list[dict]: The list of JSONs that for refused, human use and orphan medicine.
    """
    refused_json_list: list[dict] = [get_ec_json_objects(get_ec_html(HUMAN_USE_REFUSED_URL))[0],
                                     get_ec_json_objects(get_ec_html(ORPHAN_REFUSED_URL))[0]]
    return refused_json_list


def get_ec_html(url: str) -> requests.Response:
    """
    Fetches the html from a website.

    Args:
        url (str): The link to the page where the html is needed from.

    Returns:
        requests.Response: Returns a Response object that contains the response to the HTTP request.
    """
    html_active: requests.Response = requests.get(url)

    # If an http error occurred, throw error
    # TODO: Graceful handling
    html_active.raise_for_status()

    return html_active


def get_ec_json_objects(html_active: requests.Response) -> list[dict]:
    """
    Gets all the JSON objects from a web page.

    Args:
        html_active (requests.Response): The response to the HTTP request for the page where the JSONs need
            to be fetched from.

    Returns:
        list[dict]: All the JSONs on the web page are returned in a list.
    """
    soup = bs4.BeautifulSoup(html_active.text, "html.parser")

    # The data we are looking for is contained in a script tag. A JSON object containing called 'dataSet_proc'
    # We find all script tags, and isolate the one that contains the data we want.
    # We use regex, because matching on a string directly will only return *exact* matches.
    script_tag = soup.find("script", string=re.compile(r"dataSet"))

    # NOTE:
    # The website for specific medicines contains two JSON objects in the script tag.
    # "dataSet_product_information" and "dataSet_proc"
    # In this code, we are interested in the dataSet_proc.
    # However, it is possible that we are interested in the other JSON object in the future.

    # Regex "var .+?\K\[.+?\](?=;)" checks if
    #   the data is lead by 'var ', and
    #   matches '[', all items in between, and ']'
    #   and if it is closed with ;
    #   which returns the values of the two JSON objects "dataSet_product_information" and "dataSet_proc"
    plaintext_jsons = re.findall(r"var dataSet.+?\K\[.*?\](?=;)", script_tag.string, re.DOTALL)
    parsed_jsons: list[dict] = list(map(lambda plaintext: json.loads(plaintext, strict=False), plaintext_jsons))

    return parsed_jsons


def get_last_updated_date(html_active: requests.Response) -> datetime:
    """
    Gets the last updated date for a medicine on the EC website

    Args:
        html_active (requests.Response):
            html object for the webpage. Contains a string with 'Last updated on '##/##/####'

    Returns:
        (str): The date in the aforementioned string
    """
    soup = bs4.BeautifulSoup(html_active.text, "html.parser")
    last_updated_soup = soup.find(string=re.compile(f"Last updated on.*"))
    last_updated_string = last_updated_soup.text[:-1]
    return datetime.strptime(last_updated_string.split()[-1], '%d/%m/%Y')


def scrape_medicine_page(eu_num: str, html_active: requests.Response, medicine_type: MedicineType, data_folder: str) \
                                           -> (list[(str, int)], list[(str, int)], list[str], dict[str, str]):
    """
    Scrapes a medicine page for all pdf urls, urls to the ema website and attributes for a single medicine.

    Args:
        eu_num (str): Number that identifies the medicine
        html_active (requests.Response): html object that contains all html text
        medicine_type (MedicineType): The type of medicine this medicine is.
        data_folder (str): Path to the data folder

    Returns:
        (list[(str, int)], list[(str, int)], list[str], dict[str, str]):
            All the links to PDFs for decisions and annexes are
            stored in lists and returned. The same is done for all links to the ema website. All attributes are
            stored in a dictionary.
    """
    # Retrieves the html from the European Commission product page
    medicine_json, procedures_json, *_ = get_ec_json_objects(html_active)

    # Gets all the necessary information from the medicine_json and procedures_json objects
    medicine_dict, ema_url_list = get_data_from_medicine_json(medicine_json, eu_num, medicine_type)

    procedures_dict, dec_url_list, anx_url_list = get_data_from_procedures_json(procedures_json, eu_num, data_folder)

    # combine the attributes from both dictionaries files in a single JSON file
    all_attributes_dict = medicine_dict | procedures_dict

    return dec_url_list, anx_url_list, ema_url_list, all_attributes_dict


def get_data_from_medicine_json(medicine_json: dict,
                                eu_num: str,
                                medicine_type: MedicineType) \
        -> (dict[str, str], list[str]):
    """
    Gets all attribute information that is stored in the medicine JSON, and all links to the EMA website.

    The function loops through the JSON object and finds all the attributes and links,
    so that they can be used and stored. Whenever an attribute is not found, this is logged.

    Args:
        medicine_json (dict): The JSON object that contains all relevant attributes and links.
        eu_num (str): The EU number for the medicine that belongs to this JSON.
        medicine_type (MedicineType): The type of medicine that belongs to this JSON.

    Returns:
        (dict[str, str], list[str]):
            First item in the tuple is a dictionary with all the attribute values.
            The second item in the tuple is a list with all the links to the EMA.
    """
    medicine_dict: dict[str, str] = {}
    ema_url_list: list[str] = []
    # Whether current web page is about a human or orphan medicine
    human_medicine = True

    # Refused medicine never have an EU number, therefore it is set to a standard value
    medicine_dict[attr.eu_pnumber]: str = attribute_values.not_found
    # Orphan and refused medicine don't always have ATC codes, therefore it is set to a standard value
    medicine_dict[attr.atc_code] = attribute_values.not_found

    for row in medicine_json:
        match row["type"]:
            case "name":
                medicine_dict[attr.eu_aut_status]: str = row["meta"]["status_name"]
                medicine_dict[attr.eu_brand_name_current]: str = row["value"]
                if row["meta"]["status_name"] != "REFUSED":
                    medicine_dict["status_type"]: str = row["meta"]["status_type"].replace("g", "a").replace("r", "w")
                else:
                    medicine_dict["status_type"]: str = row["meta"]["status_type"]

            case "eu_num":
                if "EU/1" in row["value"]:
                    human_medicine = True
                    medicine_dict[attr.eu_pnumber] = row["value"]
                else:
                    human_medicine = False
                    medicine_dict[attr.eu_od_number]: str = row["value"]
            case "inn":
                # Sometimes the active substance is written with italics, therefore it is removed with a RegEx
                medicine_dict[attr.active_substance]: str = re.sub(re.compile('<.*?>'), '', row["value"])

            case "atc":
                medicine_dict[attr.atc_code]: str = row["meta"][0][-1]["code"]

            case "mp_link":
                medicine_dict[attr.eu_od_pnumber]: str = row["meta"]["eu_num"]
        if human_medicine:
            # Scrapes human specific attributes
            set_human_attributes(ema_url_list, medicine_dict, row)
        else:
            # Scrapes orphan specific attributes
            set_orphan_attributes(ema_url_list, medicine_dict, row)

    if MedicineType(medicine_type) == MedicineType.HUMAN_USE_ACTIVE or MedicineType(medicine_type) == \
            MedicineType.HUMAN_USE_WITHDRAWN or MedicineType(medicine_type) == MedicineType.HUMAN_USE_REFUSED:
        medicine_dict[attr.orphan_status] = "h"
    else:
        medicine_dict[attr.orphan_status] = "o"
        medicine_dict[attr.atc_code] = attribute_values.not_found

    for key, value in medicine_dict.items():
        if value == values.not_found:
            if (key == attr.eu_pnumber or key == attr.atc_code) and "EU-1" not in eu_num:
                continue
            log.warning(f"{eu_num}: No value for {key}")

    return medicine_dict, ema_url_list


def set_human_attributes(ema_url_list: list[str], medicine_dict: (dict[str, str]), row: dict):
    """
    Updates medicine_dict with attributes from the EC website for human use medicines

    Args:
        ema_url_list (list[str]): List of URLs to EMA websites
        medicine_dict (dict[str, str]): A dictionary containing all the attribute values and a list
            with all the links to the EMA.
        row (dict): Row in medicine_json to be searched
    """
    match row["type"]:
        case "mah":
            medicine_dict[attr.eu_mah_current]: str = row["value"]

        case "ema_links":
            # ema_url_list.append(row["meta"][0]["url"])

            for json_obj in row["meta"]:
                ema_url_list.append(json_obj["url"])

            # TODO: retrieve date for every PDF

        case "orphan_links":
            medicine_dict[attr.eu_orphan_con_current]: str = row["meta"]


def set_orphan_attributes(ema_url_list: list[str], medicine_dict: (dict[str, str]), row: dict):
    """
    Updates medicine_dict with attributes from the EC website for orphan medicines

    Args:
        ema_url_list (list[str]): List of URLs to EMA websites
        medicine_dict (dict[str, str]): A dictionary containing all the attribute values and a list
            with all the links to the EMA.
        row (dict): Row in medicine_json to be searched
    """
    match row["title"].lower():
        case "sponsor":
            medicine_dict[attr.eu_od_sponsor]: str = row["value"]
    match row["type"]:
        case "indication":
            medicine_dict[attr.eu_od_con]: str = row["value"]
        case "ema_links":
            for json_obj in row["meta"]:
                ema_url_list.append(json_obj["url"])
                # TODO: retrieve date for every PDF


def get_data_from_procedures_json(procedures_json: dict, eu_num: str, data_folder: str) \
                                 -> (dict[str, str], list[(str, int)], list[(str, int)]):
    """
    Gets all attribute information that is stored in the procedures JSON, and all links the decision and annex PDFs.

    The function loops through the JSON object and finds all the attributes and links,
    so that they can be used and stored. There is also some extra logic that is needed to determine some attribute
    values. This is done for the EMA number (certainty), the initial authorization type and current authorization type.
    Whenever an attribute is not found, this is logged.

    Args:
        procedures_json (dict): The JSON object that contains all relevant attributes and links
        eu_num (str): The EU number for the medicine that belongs to this JSON
        data_folder (str): Path to the data folder

    Returns:
        (dict[str, str], list[(str, int)], list[(str, int)]):
            Returns a dictionary with all the attribute values, a list
            with all the links decisions and a list with the links to the annexes.
    """
    # The necessary urls and other data will be saved in these lists and dictionary
    dec_url_list: list[(str, int)] = []
    anx_url_list: list[(str, int)] = []
    procedures_dict: dict[str, str] = {}
    # The list of ema numbers will be saved, so that the right EMA number can be chosen
    ema_numbers: list[str] = []
    # This information is needed to determine the initial authorization type
    is_exceptional: bool = False
    is_conditional: bool = False
    # This information is needed for determining the initial authorization file
    authorisation_row: int = 0
    auth_found: bool = False
    # Whether the medicine contains a file with type suspension or referral
    eu_referral = False
    eu_suspension = False
    # This information is needed to determine what the current authorization type is
    last_decision_types: list[str] = []
    last_decision_date: date = date.today() + timedelta(549)  # Safest date if there is no last_decision_date

    for row in reversed(procedures_json):
        if row["decision"]["date"] is not None:
            last_decision_date = datetime.strptime(row["decision"]["date"], f"%Y-%m-%d").date()
            break

    # for each row in the json file of each medicine, get the urls for the pdfs of the decision and annexes.
    # it also checks whether each procedure row has some information about its authorization type
    for i, row in enumerate(procedures_json):
        # Checks for initial type of authorization and keeps track if it is either Exceptional or Conditional
        if "annual reassessment" in row["type"].lower():
            is_exceptional = True
        if "annual renewal" in row["type"].lower():
            is_conditional = True
        if "centralised - authorisation" == row["type"].lower() and not auth_found:
            auth_found = True
            authorisation_row = i

        # Gets the EMA number(s) per row and puts it/them in a list
        if row["ema_number"] is not None:
            ema_numbers_row = format_ema_number(row["ema_number"])
            for en in ema_numbers_row:
                ema_numbers.append(en)

        if row["files_dec"] is None and row["files_anx"] is None:
            continue

        # Check whether one procedure has type referral
        if "referral" in row["type"].lower():
            eu_referral = True

        # Check whether one procedure has type suspension
        if "suspension" in row["type"].lower():
            eu_suspension = True

        # Parse the date, formatted as %Y-%m-%d, which looks like 1970-01-01
        decision_date: datetime = datetime.strptime(row["decision"]["date"], "%Y-%m-%d")
        decision_id = row["id"]

        if "orphan designation" == row["type"].lower():
            procedures_dict[attr.eu_od_date] = str(decision_date)
        decision_date: date = decision_date.date()
        # Puts all the decisions from the last one and a half year in a list to determine the current authorization type
        if last_decision_date - decision_date < timedelta(days=548):
            last_decision_types.append(row["type"])

        if row["files_dec"]:
            if not (any('en' in d.values() for d in row["files_dec"])):
                log.warning(f"""{eu_num}: No english file available for dec_{decision_id}""")
                add_to_non_english_file(eu_num, decision_date, "dec", row["type"].lower(), data_folder)
            else:
                pdf_url_dec = \
                    f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/dec_{decision_id}_en.pdf"""
                dec_url_list.append(("https://ec.europa.eu/health/documents/community-register/" + pdf_url_dec, i))

        if row["files_anx"]:
            if not (any('en' in d.values() for d in row["files_anx"])):
                log.warning(f"""{eu_num}: No english file available for anx_{decision_id}""")
                add_to_non_english_file(eu_num, decision_date, "anx", row["type"].lower(), data_folder)
            else:
                pdf_url_anx = \
                    f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/anx_{decision_id}_en.pdf"""
                anx_url_list.append(("https://ec.europa.eu/health/documents/community-register/" + pdf_url_anx, i))

    # Gets the oldest authorization procedure (which is the first in the list) and gets the date from there
    eu_aut_str: str = procedures_json[authorisation_row]["decision"]["date"]
    if eu_aut_str is not None:
        eu_aut_date: datetime = datetime.strptime(eu_aut_str, '%Y-%m-%d')
        eu_aut_type_initial: str = determine_initial_aut_type(eu_aut_date.year,
                                                              is_exceptional,
                                                              is_conditional)
    else:
        eu_aut_date: str = attribute_values.not_found
        eu_aut_type_initial: str = attribute_values.not_found

    # From the list of EMA numbers, the right one is chosen and its certainty determined
    if ema_numbers:
        ema_number, ema_number_certainty = determine_ema_number(ema_numbers)
    else:
        ema_number, ema_number_certainty = attribute_values.not_found, attribute_values.not_found

    # Gets ema_number_id from ema_number, removing leading 0's
    ema_number_id = ema_number.split('/')[-1].lstrip('0')
    if re.search(r'\d+/\d+', ema_number):
        ema_number_id = re.search(r'\d+/\d+', ema_number)[0].lstrip('0')

    # Currently when an attribute is not found it is simply printed to the console
    procedures_dict[attr.eu_aut_date] = str(eu_aut_date)
    procedures_dict[attr.eu_aut_type_initial] = eu_aut_type_initial
    procedures_dict[attr.eu_aut_type_current] = determine_current_aut_type(last_decision_types)
    if "od" in ema_number.lower():
        procedures_dict[attr.ema_od_number] = ema_number
        procedures_dict[attr.ema_od_number_id] = ema_number_id
    else:
        procedures_dict[attr.ema_number] = ema_number
        procedures_dict[attr.ema_number_id] = ema_number_id
    procedures_dict[attr.eu_referral] = str(eu_referral)
    procedures_dict[attr.eu_suspension] = str(eu_suspension)
    procedures_dict[attr.ema_number_certainty] = str(ema_number_certainty)
    procedures_dict[attr.authorisation_row] = str(authorisation_row)

    for key, value in procedures_dict.items():
        if value == attribute_values.not_found:
            log.warning(f"{eu_num}: No value for {key}")
    return procedures_dict, dec_url_list, anx_url_list


def add_to_non_english_file(eu_n: str, decision_date: datetime.date, filetype: str, procedure_type: str, data: str):
    """
    This function appends a line to the no_english_available.txt to make an overview of all files that don't have an
    english version.
    Args:
        eu_n (str): The short eu_n, used to form the url to the medicine page
        decision_date (datetime.date): The date of the decision.
        filetype (str): The type of the file (decision or annex)
        procedure_type (str): The procedure type of the file (as stated on the ec website)
        data (str): Path to the data folder
    """
    url = f"https://ec.europa.eu/health/documents/community-register/html/{eu_n}.htm"
    log_path = log_tools.get_log_path("no_english_available.txt", data)
    with open(log_path, "a") as f:
        f.write(f"{procedure_type}@{filetype}@{decision_date}@{url}\n")


def determine_current_aut_type(last_decision_types: list[str]) -> str:
    """
    Determines the current authorization type for a medicine

    Args:
        last_decision_types (list[str]): The decision types from the last year and a half

    Returns:
        str: The current decision type
    """
    if len(last_decision_types) > 0:
        for decision_type in last_decision_types:
            if "annual reassessment" in decision_type.lower():
                return attribute_values.aut_type_exceptional
            if "annual renewal" in decision_type.lower():
                return attribute_values.aut_type_conditional

    return attribute_values.aut_type_standard


def determine_initial_aut_type(year: int, is_exceptional: bool, is_conditional: bool) -> str:
    """
    Determines the initial authorization type, based on whether it has seen exceptional or conditional procedures

    For procedures from before 2006, it is not possible to determine the initial authorization type.
    Otherwise, the procedure type van be determined, which is either exceptional, conditional or standard.

    Args:
        year (int): The year of the first procedure.
        is_exceptional (bool): "Annual Reassessment" is among the procedures
        is_conditional (bool): "Annual renewal" is among the procedures

    Returns:
        str:
            Initial type of EU authorization.
            Can be "pre_2006", "exceptional_conditional", "exceptional", "conditional", or "standard".
    """
    if year < 2006:
        return attribute_values.NA_before
    if is_exceptional and is_conditional:
        return attribute_values.authorization_type_unknown
    if is_exceptional:
        return attribute_values.aut_type_exceptional
    if is_conditional:
        return attribute_values.aut_type_conditional
    return attribute_values.aut_type_standard


def format_ema_number(ema_number: str) -> list[str]:
    """
    Formats the input into a (list of) EMA number(s)

    In the procedures JSON file, there is often an EMA number present for a procedure, and sometimes multiple.
    The EMA numbers are formatted with a RegEx, that handles both EMA numbers for human use and orphan medicine.

    Args:
        ema_number (str): EMA number value directly fetched from the JSON, corresponding to a procedure

    Returns:
        list[str]: The list of formatted EMA numbers. Usually it only contains one EMA number, but sometimes multiple
    """
    ema_numbers: list[str] = ema_number.split(", ")
    ema_numbers_formatted: list[str] = []

    for en in ema_numbers:
        try:
            # REGEX that gets only the relevant part of the EMA numbers
            ema_number_formatted = re.findall(r"E?ME?A\/(?:H\/(?:C|\w*-\w*)\/\w*|OD\/\w*(?:\/\w*)?)", en, re.DOTALL)[0]
            ema_numbers_formatted.append(ema_number_formatted)
        except IndexError:
            continue

    return ema_numbers_formatted


def determine_ema_number(ema_numbers: list[str]) -> (str, float):
    """
    Determines the right EMA number from the list of procedures

    The right EMA number is simply the EMA number that occurs most often in the procedures table.

    Args:
        ema_numbers (list[str]): The list of formatted EMA numbers in the JSON file

    Returns:
        (str, float):
            The function returns the EMA number that occurs the most,
            and a fraction how often this EMA number is present in the list.
    """
    # gets the most frequent element in a list
    # code retrieved from https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
    ema_numbers_dict: dict[str, int] = {}
    count: int = 0
    most_occurring_item: str = attribute_values.not_found
    for item in reversed(ema_numbers):
        ema_numbers_dict[item] = ema_numbers_dict.get(item, 0) + 1
        if ema_numbers_dict[item] >= count:
            count, most_occurring_item = ema_numbers_dict[item], item

    # Calculates the fraction that have this EMA number
    fraction: float = (ema_numbers_dict.get(most_occurring_item) + 1) / (len(ema_numbers) + 1)

    return most_occurring_item, fraction


def scrape_ec(config: config_objects.WebConfig, medicine_list: list[(str, str, int, str)],
              url_file: json_helper.JsonHelper, url_refused_file: json_helper.JsonHelper):
    """
    Scrapes all medicine URLs and medicine data from the EC website

    Args:
        config (config_objects.WebConfig): Object that contains the variables that define the behaviour of webscraper
        medicine_list (list[(str, str, int, str)]): A list of medicines, structured as
            `{url, eu_num_full, medicine_type, eu_num_short}
        url_file (json_helper.JsonHelper): the dictionary containing all the urls of a specific medicine
        url_refused_file (json_helper.JsonHelper): The dictionary containing the urls of all refused files
    """

    log_path = log_tools.get_log_path("no_english_available.txt", config_objects.default_path_data)
    with open(log_path, 'w', encoding="utf-8"):
        pass  # open/clean no_english_available file

    log.info("TASK START scraping all medicine data and URLs from the EC website")
    # Transform zipped list into individual lists for thread_map function
    # The last element of the medicine_codes tuple is not of interest, thus we pop()
    with tqdm_logging.logging_redirect_tqdm():
        if config.parallelized:
            unzipped_medicine_list = [list(t) for t in zip(*medicine_list)]
            unzipped_medicine_list.pop()
            tqdm_concurrent.thread_map(url_scraper.get_urls_ec,
                                       *unzipped_medicine_list,
                                       repeat(config.path_data), repeat(url_file), repeat(url_refused_file),
                                       max_workers=cpu_count)
        else:
            for (medicine_url, eu_n, medicine_type, _) in tqdm(medicine_list):
                url_scraper.get_urls_ec(medicine_url, eu_n, medicine_type, config.path_data, url_file, url_refused_file)
    # Set empty EMA values for refused_file
    for eu_n in url_refused_file.local_dict:
        utils.init_ema_dict(eu_n, url_refused_file)
    url_file.save_dict()
    url_refused_file.save_dict()
    log.info("TASK FINISHED EC scrape")


# uncomment this when you want to test if data is retrieved for a certain medicine
"""
def debug_code(eu_num_short: str):
    ec_link = f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm"
    dec_list, anx_list, ema_list, attributes_dict = scrape_medicine_page(ec_link, MedicineType.HUMAN_USE_ACTIVE)

debug_code("h280")
"""
