import ast
import logging
import os
from pathlib import Path

import pandas as pd
import requests
from joblib import Parallel, delayed

import regex as re
import scraping.web_scraper.json_helper as json_helper

log = logging.getLogger("webscraper.ec_scraper")

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
    if epar_url != '':
        pdf_type = re.findall(r"(?<=epar-)(.*)(?=_en)", epar_url)[0]
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type]
        download_pdf_from_url(epar_url, eu_num, filename_elements)
    else:
        log.info(f"no ema documents available for {eu_num}")


def download_medicine_files(eu_n: str, url_dict: dict[str, [str]]):
    log.debug(eu_n)
    attempts = 0
    max_attempts = 4
    success = False
    attr_dict = (json_helper.JsonHelper(path=f"../../data/{eu_n}/{eu_n}_attributes.json")).load_json()
    while attempts < max_attempts and not success:
        try:
            download_pdfs_ec(eu_n, "dec", url_dict["aut_url"], attr_dict)
            download_pdfs_ec(eu_n, "anx", url_dict["smpc_url"], attr_dict)
            download_pdfs_ema(eu_n, url_dict["epar_url"], attr_dict)
            success = True
            log.info(f"Downloaded all files for {eu_n}")
        except Exception:
            attempts += 1
            log.info(f"Failed getting al pdf files for {eu_n}")


def download_all(parallel_download: bool):
    log.info("TASK START downloading pdf files from fetched urls from EC and EMA")
    urls_dict = (json_helper.JsonHelper(path="../../scraping/web_scraper/CSV/urls.json")).load_json()
    if parallel_download:
        with Parallel(n_jobs=12) as parallel:
            # Download the decision files, parallel
            parallel(
                delayed(download_medicine_files)(eu_n, urls_dict[eu_n])
                for eu_n
                in urls_dict
            )

    else:
        for eu_n in urls_dict:
            download_medicine_files(eu_n, urls_dict[eu_n])
    log.info("TASK FINISHED downloading pdf files")




