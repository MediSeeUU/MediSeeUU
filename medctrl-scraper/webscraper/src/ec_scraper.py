import json
from datetime import datetime

import regex as re
import bs4
import requests


def scrape_medicines_list(url: str) -> list[str]:
    # Links acquired from "https://ec.europa.eu/health/documents/community-register/html/index_en.htm"
    # "reg_hum_act.htm" directs to "Union Register of medicinal products for human use" | "Alphabetical"
    html_active = requests.get(url)

    # If an http error occurred, throw error
    # TODO: Graceful handling
    html_active.raise_for_status()

    soup = bs4.BeautifulSoup(html_active.text, "html.parser")

    # The data we are looking for is contained in a script tag. A JSON object containing called 'dataSet'
    # We find all script tags, and isolate the one that contains the data we want.
    # We use regex, because matching on a string directly will only return *exact* matches.
    script_tag = soup.find("script", string=re.compile(r"dataSet"))

    # Regex r"\[.*\]" matches '[', all items in between, and ']'
    # TODO: Check if script tags include other lists, make more robust.
    # TODO: Make generic helper function?
    plaintext_json: str = re.findall(r"\[.*\]", script_tag.string, re.DOTALL)[0]
    plaintext_json = plaintext_json.replace("\r", "").replace("\n", "")  # Remove newlines

    parsed_json = json.loads(plaintext_json)

    url_list = []

    # Each row has an object eu_num: { display, pre, id }
    # The URL on the EC website uses the pre and id
    for row in parsed_json:
        string_url = row['eu_num']['pre'] + row['eu_num']['id']
        url_list.append(string_url)

    return url_list


def scrape_medicine_page(url: str) -> (list[str], list[str], list[str]):
    html_active = requests.get(f"https://ec.europa.eu/health/documents/community-register/html/{url}.htm")

    # If an http error occurred, throw error
    # TODO: Graceful handling
    html_active.raise_for_status()

    soup = bs4.BeautifulSoup(html_active.text, "html.parser")

    # The data we are looking for is contained in a script tag. A JSON object containing called 'dataSet_proc'
    # We find all script tags, and isolate the one that contains the data we want.
    # We use regex, because matching on a string directly will only return *exact* matches.
    script_tag = soup.find("script", string=re.compile(r"dataSet_proc"))

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
    plaintext_json = re.findall(r"var .+?\K\[.*?\](?=;)", script_tag.string, re.DOTALL)
    for match in plaintext_json:
        match.replace("\r", "").replace("\n", "")

    # get the url linking to the EMA website, where the EPAR + OMAR files can be found. Sometimes there are two URLS
    # to the EMA website.
    medicine_json = json.loads(plaintext_json[0])
    procedures_json = json.loads(plaintext_json[1])

    print(f"Starting with {url}")

    # define lists to save the urls
    ema_url_list: list[str] = []
    dec_url_list: list[str] = []
    anx_url_list: list[str] = []

    # In the Json object from the EC, the URLs are saved in the last item in the array.
    # We still go through all lines to insure we get the right item.
    # The meta-object contains the url we are interested in.
    for row in medicine_json:
        if row["type"] == "ema_links":
            for json_obj in row["meta"]:
                ema_url_list.append(json_obj["url"])

    # for each row in the json file of each medicine, get the urls for the pdfs of the decision and annexes.
    for row in procedures_json:
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

    # TODO: Proper logging here
    print(f"Finished with {url}")
    # return the urls per medicine
    return dec_url_list, anx_url_list, ema_url_list
