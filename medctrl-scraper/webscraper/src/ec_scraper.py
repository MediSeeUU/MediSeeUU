import json
import logging
from datetime import date, datetime, timedelta
from enum import Enum

import bs4
import regex as re
import requests

log = logging.getLogger(__name__)


# This is an enum that indicates the medicine type
# TODO: file that contains all enums so that every script can make use of it
class MedicineType(Enum):
    HUMAN_USE_ACTIVE = 0
    HUMAN_USE_WITHDRAWN = 1
    ORPHAN_ACTIVE = 2
    ORPHAN_WITHDRAWN = 3


# links to the ec pages that contain medicine codes
HUMAN_USE_ACTIVE_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_hum_act.htm?sort=a"
HUMAN_USE_WITHDRAWN_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_hum_nact.htm?sort=a"
HUMAN_USE_REFUSED_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_hum_refus.htm"
ORPHAN_ACTIVE_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_od_act.htm?sort=a"
ORPHAN_WITHDRAWN_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_od_nact.htm?sort=a"
ORPHAN_REFUSED_URL: str = "https://ec.europa.eu/health/documents/community-register/html/reg_od_refus.htm"


# Gets the
def scrape_medicines_list() -> list[(str, str, int, str)]:
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


# Retrieves a list of JSON objects that are needed to make the urls for all the medicines, except the refused medicines
def scrape_active_withdrawn_jsons() -> list[json]:
    active_withdrawn_json_list: list[json] = [get_ec_json_objects(get_ec_html(HUMAN_USE_ACTIVE_URL))[0],
                                              get_ec_json_objects(get_ec_html(HUMAN_USE_WITHDRAWN_URL))[0],
                                              get_ec_json_objects(get_ec_html(ORPHAN_ACTIVE_URL))[0],
                                              get_ec_json_objects(get_ec_html(ORPHAN_WITHDRAWN_URL))[0]]

    return active_withdrawn_json_list


# Retrieves a list of JSON objects that are needed to make the urls for all the refused medicines
def scrape_refused_jsons() -> list[json]:
    refused_json_list: list[json] = [get_ec_json_objects(get_ec_html(HUMAN_USE_REFUSED_URL))[0],
                                     get_ec_json_objects(get_ec_html(ORPHAN_REFUSED_URL))[0]]

    return refused_json_list


# Fetches the html from the EC website for a certain medicine
def get_ec_html(url: str) -> requests.Response:
    html_active: requests.Response = requests.get(url)

    # If an http error occurred, throw error
    # TODO: Graceful handling
    html_active.raise_for_status()

    return html_active


# Gets the JSON object that contain all the data, links to the EMA website and links to the pdfs
def get_ec_json_objects(html_active: requests.Response) -> list[json]:
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
    

# Gets all the urls and data for a single medicine
def scrape_medicine_page(url: str, medicine_type: MedicineType) -> (list[str], list[str], list[str], dict[str, str]):
    # Retrieves the html from the European Commission product page

    html_active = get_ec_html(url)
    medicine_json, procedures_json, *_ = get_ec_json_objects(html_active)

    eu_num = get_eu_num(url)

    # Gets all the necessary information from the medicine_json and procedures_json objects
    medicine_dict, ema_url_list = get_data_from_medicine_json(medicine_json, eu_num, medicine_type)
    procedures_dict, dec_url_list, anx_url_list = get_data_from_procedures_json(procedures_json, eu_num)

    # combine the attributes from both dictionaries files in a single JSON file
    all_attributes_dict = medicine_dict | procedures_dict

    return dec_url_list, anx_url_list, ema_url_list, all_attributes_dict


# Helper function that gets the short EU number from a url
# TODO: pass the short EU number in the function, instead of retrieving it this way
def get_eu_num(url: str) -> str:
    return url.split('/')[-1].replace(".htm", "")


# The medicine_json object from the EC contains some important information that needs to be scraped
# It loops through the JSON object and finds all the attributes, so that they can be used and stored
def get_data_from_medicine_json(medicine_json: json, eu_num: str, medicine_type: MedicineType) \
        -> (dict[str, str], list[str]):
    medicine_dict: dict[str, str] = {}
    ema_url_list: list[str] = []

    # Orphan medicine don't always have ATC codes, therefore it is set to a standard value
    medicine_dict["atc_code"] = ""

    for row in medicine_json:
        match row["type"]:
            case "name":
                eu_aut_status: str = row["meta"]["status_name"]
                eu_brand_name_current: str = row["value"]
                status_type: str = row["meta"]["status_type"].replace("g", "a").replace("r", "w")

            case "eu_num":
                eu_pnumber: str = row["value"]

            case "inn":
                # Sometimes the active substance is written with italics, therefore it is removed with a RegEx
                active_substance: str = re.sub(re.compile('<.*?>'), '', row["value"])

            case "indication":
                # If at any point in the future, information about the indication needs to be stored,
                # you can do that by adding code in this section
                pass

            case "mah":
                eu_mah_current: str = row["value"]

            case "atc":
                atc_code: str = row["meta"][0][-1]["code"]

            case "ema_links":
                for json_obj in row["meta"]:
                    ema_url_list.append(json_obj["url"])
                    # TODO: retrieve date for every PDF

    # TODO: logging when an attribute is not found
    # TODO: Rewrite needed
    #       if statement could work?
    # Currently when an attribute is not found it is simply printed to the console
    try:
        medicine_dict["eu_aut_status"] = eu_aut_status
    except Exception:
        log.warning(eu_num + ": couldn't  find authorization status")
    try:
        medicine_dict["eu_brand_name_current"] = eu_brand_name_current
    except Exception:
        log.warning(eu_num + ": couldn't find current brand name")
    try:
        medicine_dict["status_type"] = status_type
    except Exception:
        log.warning(eu_num + ": couldn't find status type")
    try:
        medicine_dict["eu_pnumber"] = eu_pnumber
    except Exception:
        log.warning(eu_num + ": couldn't find EU product number")
    try:
        medicine_dict["active_substance"] = active_substance
    except Exception:
        log.warning(eu_num + ": couldn't find active substance")
    try:
        medicine_dict["eu_mah_current"] = eu_mah_current
    except Exception:
        print(eu_num + ": couldn't find current marketing authorization holder")
    if medicine_type == MedicineType.HUMAN_USE_ACTIVE or medicine_type == MedicineType.HUMAN_USE_WITHDRAWN:
        medicine_dict["orphan_status"] = "h"
        try:
            # Orphan medicine never have ATC codes, therefore it will insert a dummy value for them
            medicine_dict["atc_code"] = atc_code
        except Exception:
            log.warning(eu_num + ": couldn't find ATC code")
    else:
        medicine_dict["orphan_status"] = "o"
        medicine_dict["atc_code"] = "not applicable"

    return medicine_dict, ema_url_list


# TODO: Change this function so that it not only gets the dec and anx urls, but other data as well
def get_data_from_procedures_json(procedures_json: json, eu_num: str) -> (dict[str, str], list[str], list[str]):
    # The necessary urls and other data will be saved in these lists and dictionary
    dec_url_list: list[str] = []
    anx_url_list: list[str] = []
    procedures_dict: dict[str, str] = {}
    # The list of ema numbers will be saved, so that the right EMA number can be chosen
    ema_numbers: list[str] = []
    # This information is needed to determine the initial authorization type
    is_exceptional: bool = False
    is_conditional: bool = False
    # This information is needed to determine what the current authorization type is
    last_decision_types: list[str] = []

    for row in reversed(procedures_json):
        if row["decision"]["date"] is not None:
            last_decision_date: date = datetime.strptime(row["decision"]["date"], f"%Y-%m-%d").date()
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

        # Parse the date, formatted as %Y-%m-%d, which looks like 1970-01-01
        decision_date: date = datetime.strptime(row["decision"]["date"], f"%Y-%m-%d").date()
        decision_id = row["id"]

        # Puts all the decisions from the last one and a half year in a list to determine the current authorization type
        if last_decision_date - decision_date < timedelta(days=548):
            last_decision_types.append(row["type"])

        if row["files_dec"]:
            pdf_url_dec = f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/dec_{decision_id}_en.pdf"""
            # add url to decision pdf to list
            dec_url_list.append("https://ec.europa.eu/health/documents/community-register/" + pdf_url_dec)

        if row["files_anx"]:
            pdf_url_anx = f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/anx_{decision_id}_en.pdf"""
            # add url to annexes pdf to list
            anx_url_list.append("https://ec.europa.eu/health/documents/community-register/" + pdf_url_anx)

    # Gets the oldest authorization procedure (which is the first in the list) and gets the date from there
    try: 
        eu_aut_datetime: datetime = datetime.strptime(procedures_json[0]["decision"]["date"], '%Y-%m-%d')
        eu_aut_date: str = datetime.strftime(eu_aut_datetime, '%m-%d-%Y')
    except Exception:
        print("test")

    # From the list of EMA numbers, the right one is chosen and its certainty determined
    ema_number, ema_number_certainty = determine_ema_number(ema_numbers)

    # TODO: logging when an attribute is not found
    # Currently when an attribute is not found it is simply printed to the console
    try:
        procedures_dict["eu_aut_date"] = eu_aut_date
    except Exception:
        print(eu_num + ": couldn't find authorization date")
    try:
        procedures_dict["eu_aut_type_initial"] = determine_aut_type(eu_aut_datetime.year, is_exceptional, is_conditional)
    except Exception:
        print(eu_num + ": couldn't find initial authorization type")
    try:
        procedures_dict["eu_aut_type_current"] = determine_current_aut_type(last_decision_types)
    except Exception:
        print(eu_num + ": couldn't find current authorization type")
    try:
        procedures_dict["ema_number"] = ema_number
    except Exception:
        print(eu_num + ": couldn't find ema number")
    try:
        procedures_dict["ema_number_certainty"] = str(ema_number_certainty)
    except Exception:
        print(eu_num + ": couldn't find ema number certainty")

    return procedures_dict, dec_url_list, anx_url_list


# Determines the current authorization type
def determine_current_aut_type(last_decision_types: list[str]) -> str:
    
    for decision_type in last_decision_types:
        if "annual reassessment" in decision_type.lower():
            return "exceptional"
        if "annual renewal" in decision_type.lower():
            return "conditional"

    return "standard"


# Determines whether a medicine is exceptional, conditional or standard, based on the procedures
def determine_aut_type(year: int, is_exceptional: bool, is_conditional: bool) -> str:
    if year < 2006:
        return "pre_2006"
    if is_exceptional and is_conditional:
        return "exceptional_conditional"
    if is_exceptional:
        return "exceptional"
    if is_conditional:
        return "conditional"
    return "standard"


# EMA numbers are formatted, so that only the relevant part of the EMA number remains
# Sometimes, there are two ema numbers in one column, therefore we return a list of strings 
def format_ema_number(ema_number: str) -> list[str]:
    ema_numbers: list[str] = ema_number.split(", ")
    ema_numbers_formatted: list[str] = []

    for en in ema_numbers:
        try:
            # REGEX that gets only the relevant part of the EMA numbers
            ema_number_formatted = re.findall(r"EME?A\/(?:H\/(?:C|\w*-\w*)\/\w*|OD\/\w*(?:\/\w*)?)", en, re.DOTALL)[0]
            ema_numbers_formatted.append(ema_number_formatted)
        except IndexError:
            continue
        
    return ema_numbers_formatted


# Determines the right EMA number from the list of procedures
def determine_ema_number(ema_numbers: list[str]) -> (str, float):
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
    fraction: float = ema_numbers_dict.get(most_occurring_item) / len(ema_numbers)

    return most_occurring_item, fraction


# uncomment this when you want to test if data is retrieved for a certain medicine
"""
def test_code(eu_num_short: str):
    ec_link = f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm"
    scrape_medicine_page(ec_link)


test_code("h544")
"""
