import logging
import pathlib
import os
import json

from scraping.filter import filter
from scraping.web_scraper import __main__ as m
from scraping.web_scraper import download, ec_scraper, json_helper

# dictionaries used for mapping
key_dict = {"dec": "aut_url",
            "anx": "smpc_url",
            "public-assessment-report": "epar_url",
            "scientific-discussion": "epar_url",
            "omar": "omar_url"}

med_type_dict = {"ha": ec_scraper.MedicineType.HUMAN_USE_ACTIVE,
                 "hw": ec_scraper.MedicineType.HUMAN_USE_WITHDRAWN,
                 "oa": ec_scraper.MedicineType.ORPHAN_ACTIVE,
                 "ow": ec_scraper.MedicineType.ORPHAN_WITHDRAWN}

log = logging.getLogger("web_scraper.filter_retry")


def run_filter(n: int, data_filepath: str):
    """
    calls filter and runs retry function

    Args:
        n (int): Number of times filter is called
        data_filepath (str): the path to the data folder.
    """
    json_path = "web_scraper/"
    filter_path = ""
    # If file is run locally:
    if "web_scraper" == pathlib.Path.cwd().name:
        json_path = ""
        filter_path = "../"

    for _ in range(n):
        filter.filter_all_pdfs(data_filepath)
        url_file = json_helper.JsonHelper(path=f"{json_path}JSON/urls.json").load_json()
        retry_all(f'{filter_path}filter.txt', url_file, data_filepath)
    # remove files that can't go to the pdf parser
    filter.filter_all_pdfs(data_filepath)


def retry_all(filter_path: str, urls_file: dict[str, dict[str, list[str] | str]], data_filepath: str):
    """
    For every line in filter.txt, it scrapes the urls again.
    It also calls the download function for the specific file again

    Args:
        filter_path (str): path to filter file
        urls_file (dict[str, dict[str, list[str] | str]]): the dictionary with all the urls
        data_filepath (str): the path to the data folder
    """
    with open(filter_path, "r") as f:
        for line in f:
            filename = line.split(".pdf@")[0]
            filename_list = filename.split('_')
            eu_n = filename_list[0]
            filename_elements = filename_list[1:]
            if eu_n in urls_file:
                m.get_urls_ec(urls_file[eu_n]["ec_url"], eu_n, med_type_dict[f"{filename_elements[0]}a"],
                              data_filepath)
                retry_download(eu_n, filename_elements, urls_file[eu_n], data_filepath)


def retry_download(eu_n: str, filename_elements: list[str], url_dict: dict[str, list[str]], data_filepath: str):
    """
    Calls the download function for a specific file

    Args:
        eu_n (str): eu number used for calling the download function
        filename_elements (list[str]): filename elements, used as parameter in the download function
        url_dict (dict[str, list[str]] | dict[str, str]): dictionary that contains the url where to download from
        data_filepath (str): the path to the data folder
    """
    url = url_dict[key_dict[filename_elements[1]]]
    if len(filename_elements) == 3:
        url = url[int(filename_elements[2])]
    filedate_dict = {}
    filedates_path = f"{data_filepath}/{eu_n}/{eu_n}_filedates.json"
    target_path: str = f"{data_filepath}/{eu_n}"
    if os.path.exists(filedates_path):
        with open(filedates_path, 'r') as f:
            filedate_dict = json.load(f)
    download.download_pdf_from_url(url, eu_n, filename_elements, target_path, filedate_dict, overwrite=True)

# used for testing
# run_filter(1)
