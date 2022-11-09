import json
import logging
from scraping.web_scraper import download, ec_scraper, ema_scraper, utils, json_helper
from scraping.web_scraper import __main__ as m
from scraping.filter import pdf_filter

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

log = logging.getLogger("webscraper.filter_retry")


def run_filter(n: int, data_filepath: str = "../../data"):
    """
    calls filter and runs retry function

    Args:
        n (int): Number of times filter is called
        data_filepath (str, optional): the path to the data folder. Defaults to "../../data"
    """
    for i in range(n):
        pdf_filter.filter_all_pdfs(data_filepath)
        url_file = json_helper.JsonHelper(path="JSON/urls.json").load_json()
        retry_all('filter.txt', url_file)


def retry_all(filter_path: str, urls_file: dict[str, dict[str, list[str]]], data_filepath: str = "../../data"):
    """
    For every line in filter.txt, it scrapes the urls again.
    It also calls the download function for the specific file again

    Args:
        filter_path (str): path to filter file
        urls_file (dict[str, dict[str, list[str]]] | dict[str, dict[str, str]]): the dictionary with all the urls
        data_filepath (str): the path to the data folder
    """
    with open(filter_path, "r") as f:
        for line in f:
            filename = line.split(".pdf@")[0]
            filename_list = filename.split('_')
            eu_n = filename_list[0]
            filename_elements = filename_list[1:]
            if eu_n in urls_file:
                m.get_urls_ec(urls_file[eu_n]["ec_url"], eu_n, med_type_dict[''.join(filename_elements[:2])],
                              data_filepath)
                retry_download(eu_n, filename_elements, urls_file[eu_n])


def retry_download(eu_n: str, filename_elements: list[str], url_dict: dict[str, list[str]]):
    """
    Calls the download function for a specific file
    Args:
        eu_n (str): eu number used for calling the download function
        filename_elements (list[str]): filename elements, used as parameter in the download function
        url_dict (dict[str, list[str]] | dict[str, str]): dictionary that contains the url where to download from
    """
    url = url_dict[key_dict[filename_elements[2]]]
    if len(filename_elements) == 4:
        url = url[int(filename_elements[3])]
    utils.exception_retry(download.download_pdf_from_url, logging_instance=log)(url, eu_n, filename_elements)


# used for testing
# run_filter(3)
