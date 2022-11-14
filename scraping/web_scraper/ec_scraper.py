import json
import logging
from datetime import date, datetime, timedelta
from enum import Enum

import bs4
import regex as re
import requests

log = logging.getLogger("webscraper.ec_scraper")


# This is an enum that indicates the medicine type
# TODO: file that contains all enums so that every script can make use of it
class MedicineType(Enum):
    HUMAN_USE_ACTIVE = 0
    HUMAN_USE_WITHDRAWN = 1
    ORPHAN_ACTIVE = 2
    ORPHAN_WITHDRAWN = 3
    HUMAN_USE_REFUSED = 4
    ORPHAN_REFUSE = 5


# links to the ec pages that contain medicine codes
HUMAN_USE_ACTIVE_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_hum_act.htm?sort=a"
HUMAN_USE_WITHDRAWN_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_hum_nact.htm?sort=a"
HUMAN_USE_REFUSED_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_hum_refus.htm"
ORPHAN_ACTIVE_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_od_act.htm?sort=a"
ORPHAN_WITHDRAWN_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_od_nact.htm?sort=a"
ORPHAN_REFUSED_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_od_refus.htm"


def scrape_medicines_list() -> list[(str, str, int, str)]:
    """ Scrape the EC website, and construct urls to all individual medicine pages.

    From the EC website, the JSON files for active and withdrawn medicine are scraped. The JSONs
    contain information about the medicine that is needed to construct a link to each individual medicine page.
    It does so for all active and withdrawn, orphan and human use medicine.

    Returns:
        list[(str, str, int, str)]: The links to the medicine pages are stored in a list, along with the full EU number,
            the medicine type and a short EU number.

    """
    url_list: list[(str, str, int, str)] = []

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
            url_list.append((ec_link, eu_num_full, medicine_type, eu_num_short))
        medicine_type += 1

    # If anyone ever wants to scrape the refused medicine, the urls to these medicine can be added with this piece
    # of code
    """
    for parsed_json in scrape_refused_jsons():
        for row in parsed_json:
            eu_num_short: str = row['name']['pre'] + str(row['name']['id'])
            eu_num_full: str = "REFUSED-" + row['name']['display']

            ec_link = f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm"
            url_list.append((ec_link, eu_num_full))
            print(eu_num_full)
    """

    return url_list


def scrape_active_withdrawn_jsons() -> list[json]:
    """ Scrape the EC website for active and withdrawn medicine JSONs.

    The JSON files that are scraped are needed to construct the url to each individual medicine page.

    Returns:
        list[json]: The list of JSONs that for active and withdrawn, human use and orphan medicine.
    """
    active_withdrawn_json_list: list[json] = [get_ec_json_objects(get_ec_html(HUMAN_USE_ACTIVE_URL))[0],
                                              get_ec_json_objects(get_ec_html(HUMAN_USE_WITHDRAWN_URL))[0],
                                              get_ec_json_objects(get_ec_html(ORPHAN_ACTIVE_URL))[0],
                                              get_ec_json_objects(get_ec_html(ORPHAN_WITHDRAWN_URL))[0]]

    return active_withdrawn_json_list


def scrape_refused_jsons() -> list[json]:
    """ Scrape the EC website for refused medicine JSONs.

    The JSON files that are scraped are needed to construct the url to each individual medicine page.

    Returns:
        list[json]: The list of JSONs that for refused, human use and orphan medicine.
    """
    refused_json_list: list[json] = [get_ec_json_objects(get_ec_html(HUMAN_USE_REFUSED_URL))[0],
                                     get_ec_json_objects(get_ec_html(ORPHAN_REFUSED_URL))[0]]

    return refused_json_list


def get_ec_html(url: str) -> requests.Response:
    """ Fetches the html from a website.

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


def get_ec_json_objects(html_active: requests.Response) -> list[json]:
    """ Gets all the JSON objects from a web page.

    Args:
        html_active (requests.Response): The response to the HTTP request for the page where the JSONs need
            to be fetched from.

    Returns:
        list[json]: All the JSONs on the web page are returned in a list.
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
    plaintext_jsons = re.findall(r"var .+?\K\[.*?\](?=;)", script_tag.string, re.DOTALL)

    parsed_jsons: list[json] = list(map(lambda plaintext: json.loads(plaintext, strict=False), plaintext_jsons))
    return parsed_jsons


def scrape_medicine_page(url: str, medicine_type: MedicineType) -> (list[str], list[str], list[str], dict[str, str]):
    """ Scrapes a medicine page for all pdf urls, urls to the ema website and attributes for a single medicine.

    Args:
        url (str): The url to the medicine page for the medicine that needs to be scraped.
        medicine_type (MedicineType): The type of medicine this medicine is.

    Returns:
        (list[str], list[str], list[str], dict[str, str]): All the links to PDFs for decisions and annexes are
            stored in lists and returned. The same is done for all links to the ema website. All attributes are
            stored in a dictionary.
    """
    # Retrieves the html from the European Commission product page
    html_active = get_ec_html(url)
    medicine_json, procedures_json, *_ = get_ec_json_objects(html_active)

    # Gets the short EU number from the url
    eu_num = url.split('/')[-1].replace(".htm", "")

    # Gets all the necessary information from the medicine_json and procedures_json objects
    medicine_dict, ema_url_list = get_data_from_medicine_json(medicine_json, eu_num, medicine_type)
    procedures_dict, dec_url_list, anx_url_list = get_data_from_procedures_json(procedures_json, eu_num)

    # combine the attributes from both dictionaries files in a single JSON file
    all_attributes_dict = medicine_dict | procedures_dict

    return dec_url_list, anx_url_list, ema_url_list, all_attributes_dict


def get_data_from_medicine_json(medicine_json: dict,
                                eu_num: str,
                                medicine_type: MedicineType) \
        -> (dict[str, str], list[str]):
    """ Gets all attribute information that is stored in the medicine JSON, and all links to the EMA website.

    The function loops through the JSON object and finds all the attributes and links,
    so that they can be used and stored. Whenever an attribute is not found, this is logged.

    Args:
        medicine_json (json): The JSON object that contains all relevant attributes and links.
        eu_num (str): The EU number for the medicine that belongs to this JSON.
        medicine_type (MedicineType): The type of medicine that belongs to this JSON.

    Returns:
        (dict[str, str], list[str]): Returns a dictionary containing all the attribute values and a list
            with all the links to the EMA.
    """
    medicine_dict: dict[str, str] = {}
    ema_url_list: list[str] = []
    # Whether current web page is about a human or orphan medicine
    human_medicine = True

    # Orphan medicine don't always have ATC codes, therefore it is set to a standard value
    medicine_dict["atc_code"] = ""

    for row in medicine_json:
        match row["type"]:
            case "name":
                medicine_dict["eu_aut_status"]: str = row["meta"]["status_name"]
                medicine_dict["eu_brand_name_current"]: str = row["value"]
                medicine_dict["status_type"]: str = row["meta"]["status_type"].replace("g", "a").replace("r", "w")

            case "eu_num":
                if "EU/1" in row["value"]:
                    human_medicine = True
                    medicine_dict["eu_pnumber"]: str = row["value"]
                else:
                    human_medicine = False
                    medicine_dict["eu_od_pnumber"]: str = row["value"]

            case "inn":
                # Sometimes the active substance is written with italics, therefore it is removed with a RegEx
                medicine_dict["active_substance"]: str = re.sub(re.compile('<.*?>'), '', row["value"])

            case "indication":
                # If at any point in the future, information about the indication needs to be stored,
                # you can do that by adding code in this section
                pass

            case "atc":
                medicine_dict["atc_code"]: str = row["meta"][0][-1]["code"]

        if human_medicine:
            # Scrapes human specific attributes
            set_human_attributes(ema_url_list, medicine_dict, row)
        else:
            # Scrapes orphan specific attributes
            set_orphan_attributes(medicine_dict, row)

    if medicine_type == MedicineType.HUMAN_USE_ACTIVE or medicine_type == MedicineType.HUMAN_USE_WITHDRAWN:
        medicine_dict["orphan_status"] = "h"
    else:
        medicine_dict["orphan_status"] = "o"
        medicine_dict["atc_code"] = "not applicable"

    for key, value in medicine_dict.items():
        if value == "":
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
            medicine_dict["eu_mah_current"]: str = row["value"]

        case "ema_links":
            for json_obj in row["meta"]:
                ema_url_list.append(json_obj["url"])
                # TODO: retrieve date for every PDF


def set_orphan_attributes(medicine_dict: (dict[str, str]), row: dict):
    """
    Updates medicine_dict with attributes from the EC website for orphan medicines

    Args:
        medicine_dict (dict[str, str]): A dictionary containing all the attribute values and a list
            with all the links to the EMA.
        row (dict): Row in medicine_json to be searched
    """
    match row["title"].lower():
        case "sponsor":
            medicine_dict["sponsor"]: str = row["value"]


def get_data_from_procedures_json(procedures_json: dict, eu_num: str) -> (dict[str, str], list[str], list[str]):
    """ Gets all attribute information that is stored in the procedures JSON, and all links the decision and annex PDFs.

    The function loops through the JSON object and finds all the attributes and links,
    so that they can be used and stored. There is also some extra logic that is needed to determine some attribute
    values. This is done for the EMA number (certainty), the initial authorization type and current authorization type.
    Whenever an attribute is not found, this is logged.

    Args:
        procedures_json (json): The JSON object that contains all relevant attributes and links
        eu_num (str): The EU number for the medicine that belongs to this JSON

    Returns:
        (dict[str, str], list[str], list[str]): Returns a dictionary containing all the attribute values, a list
            with all the links decisions and a list with the links to the annexes.
    """
    # The necessary urls and other data will be saved in these lists and dictionary
    dec_url_list: list[str] = []
    anx_url_list: list[str] = []
    procedures_dict: dict[str, str] = {}
    # The list of ema numbers will be saved, so that the right EMA number can be chosen
    ema_numbers: list[str] = []
    # This information is needed to determine the initial authorization type
    is_exceptional: bool = False
    is_conditional: bool = False
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
    for row in procedures_json:
        # Checks for initial type of authorization and keeps track if it is either Exceptional or Conditional
        if "annual reassessment" in row["type"].lower():
            is_exceptional = True
        if "annual renewal" in row["type"].lower():
            is_conditional = True

        # Gets the EMA number(s) per row and puts it/them in a list
        if row["ema_number"] is not None:
            ema_numbers_row = format_ema_number(row["ema_number"])
            for en in ema_numbers_row:
                ema_numbers.append(en)

        if row["files_dec"] is None and row["files_anx"] is None:
            continue

        # Check whether one procedure has type referral
        if row["type"].lower() == "referral":
            eu_referral = True

        # Check whether one procedure has type suspension
        if row["type"].lower() == "suspension":
            eu_suspension = True

        # Parse the date, formatted as %Y-%m-%d, which looks like 1970-01-01
        decision_date: date = datetime.strptime(row["decision"]["date"], f"%Y-%m-%d").date()
        decision_id = row["id"]

        # Puts all the decisions from the last one and a half year in a list to determine the current authorization type
        if last_decision_date - decision_date < timedelta(days=548):
            last_decision_types.append(row["type"])

        if row["files_dec"]:
            if not (any('en' in d.values() for d in row["files_dec"])):
                log.warning(f"""No english file available for {eu_num}: dec_{decision_id}""")
            else:
                pdf_url_dec = \
                    f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/dec_{decision_id}_en.pdf"""
                dec_url_list.append("https://ec.europa.eu/health/documents/community-register/" + pdf_url_dec)

        if row["files_anx"]:
            if not (any('en' in d.values() for d in row["files_anx"])):
                log.warning(f"""No english file available for {eu_num}: anx_{decision_id}""")
            else:
                pdf_url_anx = \
                    f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/anx_{decision_id}_en.pdf"""
                anx_url_list.append("https://ec.europa.eu/health/documents/community-register/" + pdf_url_anx)

    # Gets the oldest authorization procedure (which is the first in the list) and gets the date from there
    eu_aut_str: str = procedures_json[0]["decision"]["date"]
    if eu_aut_str is not None:
        eu_aut_datetime: datetime = datetime.strptime(eu_aut_str, '%Y-%m-%d')
        # TODO: parse to datetime instead of string
        eu_aut_date = datetime.strftime(eu_aut_datetime, '%d-%m-%Y')
        eu_aut_type_initial: str = determine_initial_aut_type(eu_aut_datetime.year,
                                                              is_exceptional,
                                                              is_conditional)
    else:
        eu_aut_date: str = ""
        eu_aut_type_initial: str = ""

    # From the list of EMA numbers, the right one is chosen and its certainty determined
    if ema_numbers:
        ema_number, ema_number_certainty = determine_ema_number(ema_numbers)
    else:
        ema_number, ema_number_certainty = "", ""

    # Gets ema_number_id from ema_number, removing leading 0's
    ema_number_id = ema_number.split('/')[-1].lstrip('0')
    if re.search(r'\d+/\d+', ema_number):
        ema_number_id = re.search(r'\d+/\d+', ema_number)[0].lstrip('0')

    # TODO: logging when an attribute is not found
    # Currently when an attribute is not found it is simply printed to the console
    procedures_dict["eu_aut_date"] = eu_aut_date
    procedures_dict["eu_aut_type_initial"] = eu_aut_type_initial
    procedures_dict["eu_aut_type_current"] = determine_current_aut_type(last_decision_types)
    procedures_dict["ema_number"] = ema_number
    procedures_dict["ema_number_id"] = ema_number_id
    procedures_dict["eu_referral"] = str(eu_referral)
    procedures_dict["eu_suspension"] = str(eu_suspension)
    procedures_dict["ema_number_certainty"] = str(ema_number_certainty)

    for key, value in procedures_dict.items():
        if value == "":
            log.warning(f"{eu_num}: No value for {key}")

    return procedures_dict, dec_url_list, anx_url_list


def determine_current_aut_type(last_decision_types: list[str]) -> str:
    """ Determines the current authorization type for a medicine

    Args:
        last_decision_types (list[str]): The decision types from the last year and a half

    Returns:
        str: The current decision type
    """
    if len(last_decision_types) > 0:
        for decision_type in last_decision_types:
            if "annual reassessment" in decision_type.lower():
                return "exceptional"
            if "annual renewal" in decision_type.lower():
                return "conditional"

    return "standard"


def determine_initial_aut_type(year: int, is_exceptional: bool, is_conditional: bool) -> str:
    """ Determines the initial authorization type, based on whether it has seen exceptional or conditional procedures

    For procedures from before 2006, it is not possible to determine the initial authorization type.
    Otherwise, the procedure type van be determined, which is either exceptional, conditional or standard.

    Args:
        year (int): The year of the first procedure.
        is_exceptional (bool): _description_
        is_conditional (bool): _description_

    Returns:
        str: _description_
    """
    if year < 2006:
        return "pre_2006"
    if is_exceptional and is_conditional:
        return "exceptional_conditional"
    if is_exceptional:
        return "exceptional"
    if is_conditional:
        return "conditional"
    return "standard"


def format_ema_number(ema_number: str) -> list[str]:
    """ Formats the input into a (list of) EMA number(s)

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
        # TODO: Replace exception with specific exceptions
        except Exception:
            continue

    return ema_numbers_formatted


def determine_ema_number(ema_numbers: list[str]) -> (str, float):
    """ Determines the right EMA number from the list of procedures

    The right EMA number is simply the EMA number that occurs most often in the procedures table.

    Args:
        ema_numbers (list[str]): The list of formatted EMA numbers in the JSON file

    Returns:
        (str, float): The function returns the EMA number that occurs the most, and a fraction how often
            this EMA number is present in the list.
    """
    # gets the most frequent element in a list
    # code retrieved from https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
    ema_numbers_dict: dict[str, int] = {}
    count: int = 0
    most_occurring_item: str = ""
    for item in reversed(ema_numbers):
        ema_numbers_dict[item] = ema_numbers_dict.get(item, 0) + 1
        if ema_numbers_dict[item] >= count:
            count, most_occurring_item = ema_numbers_dict[item], item

    # Calculates the fraction that have this EMA number
    fraction: float = (ema_numbers_dict.get(most_occurring_item) + 1) / (len(ema_numbers) + 1)

    return most_occurring_item, fraction


# uncomment this when you want to test if data is retrieved for a certain medicine
"""
def debug_code(eu_num_short: str):
    ec_link = f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm"
    dec_list, anx_list, ema_list, attributes_dict = scrape_medicine_page(ec_link, MedicineType.HUMAN_USE_ACTIVE)

debug_code("h280")
"""
