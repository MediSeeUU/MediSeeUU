import logging
from pathlib import Path

import regex as re
import requests
import tqdm
import tqdm.contrib.concurrent as tqdm_concurrent
import tqdm.contrib.logging as tqdm_logging

import scraping.web_scraper.json_helper as json_helper
import scraping.web_scraper.utils as utils

log = logging.getLogger("webscraper.ec_scraper")
urls_file: json_helper.JsonHelper

# TODO: make sure the data path is declared somewhere in main.
data_path = '../../data'


def download_pdf_from_url(url: str, eu_num: str, filename_elements: list[str]):
    downloaded_file = requests.get(url)
    downloaded_file.raise_for_status()
    filename: str = f"{eu_num}_{'_'.join(filename_elements)}.pdf"

    # TODO: Runs this check for every downloaded file. Could be more efficient?
    path_medicine = Path(f"{data_path}/{eu_num}")
    path_medicine.mkdir(exist_ok=True)
    with open(f"{data_path}/{eu_num}/{filename}", "wb") as file:
        file.write(downloaded_file.content)
        log.debug(f"DOWNLOADED {filename} for {eu_num}")


# Download pdfs using the dictionaries created from the json file
def download_pdfs_ec(eu_num: str, pdf_type: str, pdf_urls: list[str], med_dict: dict[str, str]):
    file_counter = 0
    for url in pdf_urls:
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type, str(file_counter)]
        download_pdf_from_url(url, eu_num, filename_elements)
        file_counter += 1


def download_pdfs_ema(eu_num: str, epar_url: str, med_dict: dict[str, str]):
    if epar_url == '':
        log.info(f"no ema documents available for {eu_num}")
    else:
        pdf_type = re.findall(r"(?<=epar-)(.*)(?=_en)", epar_url)[0]
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type]
        download_pdf_from_url(epar_url, eu_num, filename_elements)


def download_medicine_files(eu_n: str, url_dict: dict[str, [str]]):
    attr_dict = (json_helper.JsonHelper(path=f"{data_path}/{eu_n}/{eu_n}_attributes.json")).load_json()
    utils.exception_retry(download_pdfs_ec, logging_instance=log)(eu_n, "dec", url_dict["aut_url"], attr_dict)
    utils.exception_retry(download_pdfs_ec, logging_instance=log)(eu_n, "anx", url_dict["smpc_url"], attr_dict)
    utils.exception_retry(download_pdfs_ema, logging_instance=log)(eu_n, url_dict["epar_url"], attr_dict)
    log.info(f"Finished download for {eu_n}")


def download_all(url_jsonhelper: json_helper.JsonHelper, parallel_download: bool):
    global urls_file
    urls_file = url_jsonhelper

    with tqdm_logging.logging_redirect_tqdm():
        if parallel_download:
            tqdm_concurrent.thread_map(download_medicine_files,
                                       urls_file.local_dict.keys(),
                                       urls_file.local_dict.values(), max_workers=12)

        else:
            for eu_n, urls_eu_n_dict in tqdm.tqdm(urls_file.local_dict.items()):
                download_medicine_files(eu_n, urls_eu_n_dict)
