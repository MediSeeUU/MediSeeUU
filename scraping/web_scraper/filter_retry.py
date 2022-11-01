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

# path to data. TODO: make sure it gets it from the main
data_filepath = "../../data"
log = logging.getLogger("webscraper.filter_retry")


def run_filter(n: str):
    """
    calls filter and runs retry function

    Args:
        n: Number of times filter is called

    Returns:
        None
    """
    for i in range(n):
        pdf_filter.filter_all_pdfs(data_filepath)
        url_file = json_helper.JsonHelper(path="JSON/urls.json").load_json()
        retry_all('filter.txt', url_file)


def retry_all(filter_path: str, url_jsonhelper: json_helper.JsonHelper):
    """
    For every line in filter.txt, it scrapes the urls again.
    It also calls the download function for the specific file again

    Args:
        filter_path: path to filter file
        url_jsonhelper: the dictionary with all the urls

    Returns:
        None
    """
    urls_file = url_jsonhelper
    with open(filter_path, "r") as f:
        for line in f:
            filename = line.split(".pdf@")[0]
            filename_list = filename.split('_')
            eu_n = filename_list[0]
            filename_elements = filename_list[1:]
            m.get_urls_ec(urls_file[eu_n]["ec_url"], eu_n, med_type_dict[''.join(filename_elements[:2])], data_filepath)
            if eu_n in urls_file:
                retry_download(eu_n, filename_elements, urls_file[eu_n])


def retry_download(eu_n, filename_elements, url_dict: dict[str, list[str]]):
    """

    Args:
        eu_n: eu number used for calling the download function
        filename_elements: filename elements, used as parameter in the download function
        url_dict: dictionary that contains the url where to download from

    Returns:
        None
    """
    url = url_dict[key_dict[filename_elements[2]]]
    if len(filename_elements) == 4:
        url = url[int(filename_elements[3])]
    utils.exception_retry(download.download_pdf_from_url, logging_instance=log)(url, eu_n, filename_elements)


#used for testing
run_filter(3)


