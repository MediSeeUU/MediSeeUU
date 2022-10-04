import json
import sys
import os
from datetime import datetime

import bs4
import regex as re
import requests

def scrape_medicine_urls(url: str):
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
    plaintext_json: str = re.findall(r"\[.*\]", script_tag.text, re.DOTALL)[0]
    plaintext_json = plaintext_json.replace("\r", "").replace("\n", "")  # Remove newlines

    parsed_json = json.loads(plaintext_json)

    url_list = []

    # Each row has an object eu_num: { display, pre, id }
    # The URL on the EC website uses the pre and id
    for row in parsed_json:
        string_url = row['eu_num']['pre'] + row['eu_num']['id']
        url_list.append(string_url)

    return url_list


def get_urls_for_pdf_and_ema(url: str):
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

    # Regex r"(?<=var .+?)\[.+?\](?=;)" checks if 
    #   the data is lead by 'var ', and 
    #   matches '[', all items in between, and ']'
    #   and if it is closed with a ;
    #   which returns the values of the two JSON objects "dataSet_product_information" and "dataSet_proc"
    plaintext_json = re.findall(r"(?<=var .+?)\[.+?\](?=;)", script_tag.text, re.DOTALL)
    for match in plaintext_json:
        match = match.replace("\r", "").replace("\n", "")  # Remove newlines

    # get the url linking to the EMA website, where the EPAR + OMAR files can be found. Sometimes there are two URLS
    # to the EMA website.
    ema_url_list = (re.findall(r"\w+:\/\/[-a-zA-Z0-9:@;?&=\/%\+\.\*!'\(\),\$_\{\}\^~\[\]`#|]+", plaintext_json[0]))
    procedures_json = json.loads(plaintext_json[1])

    # save prints to file
    original_stdout = sys.stdout
    sys.stdout = open('log.txt', 'w')

    print(f"Starting with {url}")

    # define lists to save the urls
    dec_url_list = []
    anx_url_list = []

    # for each row in the json file of each medicine, get the urls for the pdfs of the decision and annexes.
    for row in procedures_json:
        if row["files_dec"] is None and row["files_anx"] is None:
            continue

        decision_date = datetime.strptime(row["decision"]["date"], f"%Y-%m-%d").date()
        decision_id = row["id"]

        if row["files_dec"]:
            pdf_url_dec = f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/dec_{decision_id}_en.pdf"""
            # add url to decision pdf to list
            dec_url_list.append("https://ec.europa.eu/health/documents/community-register/" + pdf_url_dec)
            # NOTE: if you want to download the PDFs immediately while getting the URLs:
            # downloadDecPDFfromURL(url, pdf_url_dec, decision_id)

        if row["files_anx"]:
            pdf_url_anx = f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/anx_{decision_id}_en.pdf"""
            # add url to annexes pdf to list
            anx_url_list.append("https://ec.europa.eu/health/documents/community-register/" + pdf_url_anx)
            # NOTE: if you want to download the PDFs immediately while getting the URLs:
            # downloadAnnPDFfromURL(url, pdf_url_anx, decision_id)

    # TODO: Proper logging here
    print(f"Finished with {url}")
    sys.stdout = original_stdout
    # return the urls per medicine
    return dec_url_list, anx_url_list, ema_url_list


# In the end the string will look like:
# https://ec.europa.eu/health/documents/community-register/2004/200404287648/dec_7648_en.pdf
# TODO: Graceful failure on failed request
# TODO: Retry on failed request

def download_pdf_from_url(med_id: str, url: str, pdf_type: str):
    downloaded_file = requests.get(url)
    dec_id = re.findall(rf"(?<={pdf_type}_)\d+", url)[0]
    if pdf_type == "dec":
        with open(f"./data/authorisation_decisions/{med_id}_dec_{dec_id}.pdf", "wb") as file:
            file.write(downloaded_file.content)
            # print(f"  Downloaded {dec_id} decision")
    elif pdf_type == "anx":
        with open(f"./data/annexes/{med_id}_anx_{dec_id}.pdf", "wb") as file:
            file.write(downloaded_file.content)
            # print(f"  Downloaded {dec_id} annex")

# NOTE: Below the old download code:
# def downloadDecPDFfromURL(url: str, pdf_url_dec: str, decision_id):
#     downloaded_file = requests.get("https://ec.europa.eu/health/documents/community-register/" + pdf_url_dec)
#     with open(f"./data/authorisation_decisions/{url}_dec_{decision_id}.pdf", "wb") as file:
#             file.write(downloaded_file.content)
#             print(f"  Downloaded {decision_id} decision")

# def downloadAnnPDFfromURL(url: str, pdf_url_anx: str, decision_id):
#     downloaded_file = requests.get("https://ec.europa.eu/health/documents/community-register/" + pdf_url_anx)
#     with open(f"./data/annexes/{url}_anx_{decision_id}.pdf", "wb") as file:
#         file.write(downloaded_file.content)
#         print(f"  Downloaded {decision_id} annex")
