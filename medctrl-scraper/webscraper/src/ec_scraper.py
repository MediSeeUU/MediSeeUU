import json
from datetime import date, datetime
from re import DOTALL
from typing import Type

import regex as re
import bs4
import requests


def scrape_medicines_list(url: str) -> list[(str, str)]:
    # Links acquired from "https://ec.europa.eu/health/documents/community-register/html/index_en.htm"
    # "reg_hum_act.htm" directs to "Union Register of medicinal products for human use" | "Alphabetical"
    html_active = get_ec_html(url)
    parsed_json, *_ = get_ec_json_objects(html_active)

    url_list: list[(str, str)] = []

    # Each row has an object eu_num: { display, pre, id }
    # The URL on the EC website uses the pre and id
    for row in parsed_json:
        eu_num_short: str = row['eu_num']['pre'] + row['eu_num']['id']
        eu_num_full: str = (row['eu_num']['display']).replace("/", "-")

        ec_link = f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm"
        url_list.append((ec_link, eu_num_full))

    return url_list


def scrape_medicine_page(url: str) -> (list[str], list[str], list[str], dict[str, str]):
    # Retrieves the html from the European Commission product page
    html_active = get_ec_html(url)
    medicine_json, procedures_json, *_ = get_ec_json_objects(html_active)

    # Gets all the necessary information from the medicine_json and procedures_json objects
    medicine_dict, ema_url_list = get_data_from_medicine_json(medicine_json)
    procedures_dict, dec_url_list, anx_url_list = get_data_from_procedures_json(procedures_json)

    return dec_url_list, anx_url_list, ema_url_list, medicine_dict, procedures_dict


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

    parsed_jsons: list[json] = list(map(lambda plaintext: json.loads(plaintext), plaintext_jsons))
    return parsed_jsons


# The medicine_json object from the EC contains some important information that needs to be scraped
# It loops through the JSON object and finds all the attributes, so that they can be used and stored
def get_data_from_medicine_json(medicine_json: json) -> (dict[str, str], list[str]):
    medicine_dict: dict[str, str] = {}
    ema_url_list: list[str] = []

    # Orphan medicine don't always have ATC codes, therefore it is set to a standard value
    medicine_dict["atc_code"] = None

    for row in medicine_json:
        match row["type"]:
            case "name":
                medicine_dict["eu_aut_status"] = row["meta"]["status_name"]
                medicine_dict["eu_brand_name_current"] = row["value"]

            case "eu_num":
                medicine_dict["eu_pnumber"] = row["value"]

            case "inn":
                medicine_dict["active_substance"] = row["value"]

            case "indication":
                # If at any point in the future, information about the indication needs to be stored,
                # you can do that by adding code in this section
                pass

            case "mah":
                medicine_dict["eu_mah_current"] = row["value"]

            case "atc":
                meta_obj = row["meta"][0]
                medicine_dict["atc_code"] = meta_obj[-1]["code"]

            case "ema_links":
                for json_obj in row["meta"]:
                    ema_url_list.append(json_obj["url"])

    return medicine_dict, ema_url_list


# TODO: Change this function so that it not only gets the dec and anx urls, but other data as well
def get_data_from_procedures_json(procedures_json: json) -> (list[str, str], list[str], list[str]):
    dec_url_list: list[str] = []
    anx_url_list: list[str] = []
    procedures_dict: list[str, str] = {}
    is_exceptional: bool = False
    is_conditional: bool = False
    ema_numbers: list[str] = []

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
        decision_date = datetime.strptime(row["decision"]["date"], f"%Y-%m-%d").date()
        decision_id = row["id"]

        if row["files_dec"]:
            pdf_url_dec = f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/dec_{decision_id}_en.pdf"""
            # add url to decision pdf to list
            dec_url_list.append("https://ec.europa.eu/health/documents/community-register/" + pdf_url_dec)

        if row["files_anx"]:
            pdf_url_anx = f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/anx_{decision_id}_en.pdf"""
            # add url to annexes pdf to list
            anx_url_list.append("https://ec.europa.eu/health/documents/community-register/" + pdf_url_anx)

    # Gets the oldest authorization procedure (which is the first in the list) and gets the date from there
    eu_aut_date: datetime = datetime.strptime(procedures_json[0]["decision"]["date"], '%Y-%m-%d')

    # From the list of EMA numbers, the right one is chosen and its certainty determined
    ema_number, ema_number_certainty = determine_ema_number(ema_numbers)

    # All the attribute values are put in the dictionary
    procedures_dict["eu_aut_date"] = datetime.strftime(eu_aut_date, f"%d-%m-%Y")
    procedures_dict["eu_aut_type_initial"] = determine_aut_type(eu_aut_date.year, is_exceptional, is_conditional)
    # procedures_dict["eu_aut_type_current"] TODO: Ask in data meeting
    procedures_dict["ema_number"] = ema_number
    procedures_dict["ema_number_certainty"] = str(ema_number_certainty)

    return procedures_dict, dec_url_list, anx_url_list


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
    ema_numbers: list[str]= ema_number.split(", ")
    ema_numbers_formatted: list[str] = []

    for en in ema_numbers:
        # REGEX that gets only the relevant part of the EMA numbers
        ema_number_formatted = re.findall(r"EME?A\/(?:H\/(?:C|\w*-\w*)\/\w*|OD\/\w*(?:\/\w*)?)", en, re.DOTALL)[0]
        ema_numbers_formatted.append(ema_number_formatted)

    return ema_numbers_formatted

# Determines the right EMA number from the list of procedures
# TODO: implement this function
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


def test_code(eu_num_short):
    ec_link = f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm"
    scrape_medicine_page(ec_link)


# uncomment this when you want to test if data is retrieved for a certain medicine
test_code("h1367")
