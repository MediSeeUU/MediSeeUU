import json
import logging
import os

import tqdm.contrib.logging as tqdm_logging
from tqdm import tqdm

import scraping.utilities.definitions.attributes as attr
import scraping.utilities.log.log_tools as log_tools
from scraping.filter import filter
from scraping.utilities.web import json_helper, medicine_type as med_type
from scraping.utilities.web.medicine_type import MedicineType
from scraping.web_scraper import download, url_scraper

# dictionaries used for mapping
key_dict = {"dec": attr.aut_url,
            "anx": attr.smpc_url}

med_type_dict = {"ha": MedicineType.HUMAN_USE_ACTIVE,
                 "hw": MedicineType.HUMAN_USE_WITHDRAWN,
                 "oa": MedicineType.ORPHAN_ACTIVE,
                 "ow": MedicineType.ORPHAN_WITHDRAWN}

log = logging.getLogger("web_scraper.filter_retry")


def run_filter(n: int, data_filepath: str):
    """
    calls filter and runs retry function

    Args:
        n (int): Number of times filter is called
        data_filepath (str): the path to the data folder.
    """
    data_filepath = f"{data_filepath}/active_withdrawn"
    parent_path = data_filepath.split("data")[0]
    json_path = f"{parent_path}scraping/web_scraper/JSON"
    filter.filter_all_pdfs(data_filepath)
    for _ in range(n):
        url_file = json_helper.JsonHelper(path=f"{json_path}/urls.json")
        url_refused_file = json_helper.JsonHelper(path=f"{json_path}/refused_urls.json")
        data_folder = data_filepath.split("active_withdrawn")[0]
        filter_path = log_tools.get_log_path("filter.txt", data_folder)
        with open(filter_path, "r") as f:
            filter_lines = f.read().split('\n')
            with tqdm_logging.logging_redirect_tqdm():
                for line in tqdm(filter_lines):
                    retry_medicine(line, url_file, data_folder, url_refused_file)
                filter.filter_all_pdfs(data_filepath, filter_lines)


def retry_medicine(filter_line: str, url_file: json_helper.JsonHelper, data_filepath: str,
                   url_refused_file: json_helper.JsonHelper):
    """
    For every line in filter.txt, it scrapes the urls again.
    It also calls the download function for the specific file again

    Args:
        filter_line(list[str]): line in filter.txt containing the EU number of medicine to download again
        url_file (json_helper.JsonHelper): the dictionary with all the urls
        data_filepath (str): the path to the data folder
        url_refused_file (json_helper.JsonHelper): dictionary with all refused urls
    """
    filename = filter_line.split(".pdf@")[0]
    filename_list = filename.split('_')
    eu_n = filename_list[0]
    filename_elements = filename_list[1:]
    url_dict = url_file.load_json()
    if eu_n in url_dict:
        url_scraper.get_urls_ec(url_dict[eu_n][attr.ec_url], eu_n, med_type_dict[f"{filename_elements[0]}a"],
                                data_filepath, url_file, url_refused_file)
        retry_download(eu_n, filename_elements, url_dict[eu_n], data_filepath)


def retry_download(eu_n: str, filename_elements: list[str], url_dict: dict[str, list[str]], data_filepath: str):
    """
    Calls the download function for a specific file

    Args:
        eu_n (str): eu number used for calling the download function
        filename_elements (list[str]): filename elements, used as parameter in the download function
        url_dict (dict[str, list[str]] | dict[str, str]): dictionary that contains the url where to download from
        data_filepath (str): the path to the data folder
    """
    filename_type = filename_elements[1]

    for epar_str in med_type.epar_priority_list:
        key_dict[epar_str] = attr.epar_url
    for omar_str in med_type.omar_priority_list:
        key_dict[omar_str] = attr.omar_url
    for odwar_str in med_type.odwar_priority_list:
        key_dict[odwar_str] = attr.odwar_url

    if filename_type in key_dict.keys():
        url = url_dict[key_dict[filename_type]]
        if len(filename_elements) == 3:
            url = url[int(filename_elements[2])]
    else:
        url = url_dict[attr.other_ema_urls]
        if len(filename_elements) == 3:
            url = url[int(filename_elements[2])][0]
    # Get nth file if file has number in name

    webdata_dict = {}
    webdata_path = f"{data_filepath}/active_withdrawn/{eu_n}/{eu_n}_webdata.json"
    target_path: str = f"{data_filepath}/active_withdrawn/{eu_n}"
    if os.path.exists(webdata_path):
        with open(webdata_path, 'r') as f:
            webdata_dict = json.load(f)
    download.download_pdf_from_url(url, eu_n, filename_elements, target_path, webdata_dict, overwrite=True)
