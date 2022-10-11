import json
from datetime import date, datetime
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
    dec_url_list, anx_url_list = get_data_from_procedures_json(procedures_json)

    return dec_url_list, anx_url_list, ema_url_list, medicine_dict


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
    # set some predefined values. Whenever this function doesn't find the data
    # it makes sure it doesn't cause an error
    # TODO: proper error handling

    medicine_dict: dict[str, str] = {}
    ema_url_list: list[str] = []

    for row in medicine_json:
        match row["type"]:
            case "name":
                medicine_dict["status"] = row["meta"]["status_name"]
                medicine_dict["name"] = row["value"]

            case "eu_num":
                medicine_dict["eu_num"] = row["value"]

            case "inn":
                medicine_dict["active_substance"] = row["value"]

            case "indication":
                # If at any point in the future, information about the indication needs to be stored,
                # you can do that by adding code in this section
                pass

            case "mah":
                medicine_dict["market_auth_holder"] = row["value"]

            case "atc":
                meta_obj = row["meta"][0]
                medicine_dict["atc_code"] = meta_obj[-1]["code"]

            case "ema_links":
                for json_obj in row["meta"]:
                    ema_url_list.append(json_obj["url"])

    return medicine_dict, ema_url_list


# TODO: Change this function so that it not only gets the dec and anx urls, but other data as well
def get_data_from_procedures_json(procedures_json: json) -> (list[str], list[str]):
    dec_url_list: list[str] = []
    anx_url_list: list[str] = []

    # set some predefined values. Whenever this function doesn't find the data
    # it makes sure it doesn't cause an error
    # TODO: propper error handling
    try:
        eu_aut_date: date = datetime.strptime(procedures_json[0]["decision"]["date"], f"%Y-%m-%d").date()
    except TypeError:
        print("This medicine does't have any procedures")
    except:
        print("something went wrong with fetching the authorization date")

    eu_aut_type_initial = None    # TODO: vragen of zowel exceptional als conditonal mogelijk is

    # Checks if the last procedure contains Annual Reassesment or Annual Renewal in its name, and decides the authorization type accordingly
    eu_aut_type_current = decide_aut_type(eu_aut_date.year, True if "Annual Reassesment" in procedures_json[-1]["type"] else False, True if "Annual Renewal" in procedures_json[-1]["type"] else False)
    ema_numbers = [] # TODO: nachecken of het echt het meest voorkomende nummer moet zijn, of gewoon het laatst voorkomende
    #re.findall(r"EMEA.{5}\w+", procedures_json[-1]["ema_number"], re.DOTALL)[0]
    ema_number_certainty: float = None

    # Variables for checking the eu_aut_type_initial
    isConditional: bool = False
    isExceptional: bool = False

    # for each row in the json file of each medicine, get the urls for the pdfs of the decision and annexes.
    # it also checks whether each procedure row has some information about its authorization type
    for row in procedures_json: 

        # Checks whether the medicine has 
        if "annual reassesment" in row["type"].lower():
            isExceptional = True

        if "annual renewal" in row["type"].lower():
            isConditional = True

        if row["files_dec"] is None and row["files_anx"] is None:
            continue

        ema_numbers.append(row["ema_number"])

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

    eu_aut_type_initial = decide_aut_type(eu_aut_date.year, isExceptional, isConditional)

    # Filters out all empty ema numbers
    ema_numbers = [x for x in ema_numbers if x != None]

    for x in ema_numbers:
        print(x)

    return dec_url_list, anx_url_list


# Determines whether a medicine is exceptional, conditional or standard, based on the procedures
def decide_aut_type(year: int, isExceptional: bool, isConditional: bool) -> str:
    if year < 2006:
        return "pre2006"
    if isExceptional and isConditional:
        return "exceptionalAndConditional"
    if isExceptional:
        return "exceptional"
    if isConditional:
        return "conditional"
    return "standard"

# uncomment this when you want to test if data is retrieved for a certain medicine
#scrape_medicine_page("o218")
