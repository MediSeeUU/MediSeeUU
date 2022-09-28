import requests
import bs4
import re
import json
from datetime import datetime

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
    # We use regex, because mathing on a string directly will only return *exact* matches.
    scriptTag = soup.find("script", string=re.compile(r"dataSet"))

    # Regex r"\[.*\]" matches '[', all items in between, and ']'
    # TODO: Check if script tags include other lists, make more robust.
    plaintext_json: str = re.findall(r"\[.*\]", scriptTag.text, re.DOTALL)[0]
    plaintext_json      = plaintext_json.replace("\r", "").replace("\n", "") # Remove newlines

    parsed_json = json.loads(plaintext_json)

    url_list = []

    # Each row has an object eu_num: { display, pre, id }
    # The URL on the EC website uses the pre and id
    for row in parsed_json:
        string_url = row['eu_num']['pre'] + row['eu_num']['id']
        url_list.append(string_url)
        
    return url_list


def getPDF_from_medicine(url: str):
    html_active = requests.get(f"https://ec.europa.eu/health/documents/community-register/html/{url}.htm")

    # If an http error occurred, throw error
    # TODO: Graceful handling
    html_active.raise_for_status()

    soup = bs4.BeautifulSoup(html_active.text, "html.parser")
    
    # The data we are looking for is contained in a script tag. A JSON object containing called 'dataSet_proc'
    # We find all script tags, and isolate the one that contains the data we want.
    # We use regex, because mathing on a string directly will only return *exact* matches.
    scriptTag = soup.find("script", string=re.compile(r"dataSet_proc"))

    # NOTE:
    # The website for specific medicines contains two JSON objects in the script tag.
    # "dataSet_product_information" and "dataSet_proc"
    # In this code, we are interested in the dataSet_proc.
    # However, it is possible that we are interested in the other JSON object in the future.

    # Regex r"(?<=dataSet_proc = )\[.*\]" checks if 
    #   the data is lead by 'dataSet_proc = ' 
    #   matches '[', all items in between, and ']'
    plaintext_json = re.findall(r"(?<=dataSet_proc = )\[.*\]", scriptTag.text, re.DOTALL)[0]
    plaintext_json = plaintext_json.replace("\r", "").replace("\n", "") # Remove newlines

    procedures_json = json.loads(plaintext_json)
    
    for row in procedures_json:
        decision_date = datetime.strptime(row["decision"]["date"], f"%Y-%m-%d").date()
        decision_id   = row["id"]
    
        if row["files_dec"]:
            pdf_url_dec = f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/dec_{decision_id}_en.pdf"""
            
            # TODO: Graceful failure on failed request
            # TODO: Retry on failed request
            downloaded_file = requests.get("https://ec.europa.eu/health/documents/community-register/" + pdf_url_dec)
            with open(f"./data/authorisation_decisions/{url}_dec_{decision_id}.pdf", "wb") as file:
                file.write(downloaded_file.content)
                
                
        if row["files_anx"]:
            # In the end the string will look like: https://ec.europa.eu/health/documents/community-register/2004/200404287648/dec_7648_en.pdf
            pdf_url_anx = f"""{decision_date.year}/{decision_date.strftime("%Y%m%d")}{decision_id}/anx_{decision_id}_en.pdf"""
            
            downloaded_file = requests.get("https://ec.europa.eu/health/documents/community-register/" + pdf_url_anx)
            with open(f"./data/authorisation_decisions/{url}_anx_{decision_id}.pdf", "wb") as file:
                file.write(downloaded_file.content)
        
        # TODO: Proper logging here