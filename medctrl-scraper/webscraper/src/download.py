import pandas as pd
from joblib import Parallel, delayed
import requests
import regex as re
import ast
from pathlib import Path

import sys
import os
import logging

from requests import Response

log = logging.getLogger(__name__)


def download_pdf_from_url(url: str, eu_num: str, filename_elements: list[str]):
    downloaded_file = requests.get(url)
    filename: str = f"{eu_num}_{'_'.join(filename_elements)}.pdf"

    # TODO: Runs this check for every downloaded file. Could be more efficient?
    path_medicine = Path(f"../data/medicines/{eu_num}")
    path_medicine.mkdir(exist_ok=True)
    with open(f"../data/medicines/{eu_num}/{filename}", "wb") as file:
        file.write(downloaded_file.content)
        log.debug(f"DOWNLOADED {filename} for {eu_num}")


# Download pdfs using the dictionaries created from the CSV files
def download_pdfs_ec(eu_num: str, pdf_type: str, pdf_type_dict: dict(), med_dict: dict()):
    file_counter = 0
    for url in ast.literal_eval(pdf_type_dict[eu_num]):
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type, str(file_counter)]
        download_pdf_from_url(url, eu_num, filename_elements)
        file_counter += 1


def download_pdfs_ema(eu_num: str, epar_dict: dict(), med_dict: dict()):
    if eu_num in epar_dict:
        url = epar_dict[eu_num]
        pdf_type = re.findall(r"(?<=epar-)(.*)(?=_en)", url)[0]
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type]
        download_pdf_from_url(url, eu_num, filename_elements)
    else:
        log.info(f"no ema documents available for {eu_num}")


# Function for reading the CSV contents back into dictionaries that can be used for downloading.
def read_csv_files():
    dec = pd.read_csv('../data/CSV/decision.csv', header=None, index_col=0).squeeze().to_dict()
    anx = pd.read_csv('../data/CSV/annexes.csv', header=None, index_col=0).squeeze().to_dict()
    epar = pd.read_csv('../data/CSV/epar.csv', header=None, index_col=0).squeeze().to_dict()
    med_dict = pd.read_csv('../data/CSV/med_dict.csv', header=None, index_col=0).squeeze().to_dict()
    return dec, anx, epar, med_dict


# TODO: Add a new function in a way that that function gets a medicine and downloads all files for that medicine.
def download_medicine_files(eu_n: str, dec: dict(), anx: dict(), epar: dict(), med_info: dict()):
    attempts = 0
    max_attempts = 4
    success = False
    while attempts < max_attempts and not success:
        try:
            download_pdfs_ec(eu_n, "dec", dec, med_info)
            download_pdfs_ec(eu_n, "anx", anx, med_info)
            download_pdfs_ema(eu_n, epar, med_info)
            success = True
            log.info(f"Downloaded all files for {eu_n}")
        except Exception:
            attempts += 1
            log.info(f"Failed getting al pdf files for {eu_n}")


# TODO: Fix downloading for epar files
def download_all(parallel: bool):
    # Store the result of the csv converting into dictionaries
    decisions, annexes, epar, med_dict = read_csv_files()
    if parallel:
        Parallel(n_jobs=12)(delayed(download_medicine_files)
                            (eu_n, decisions, annexes, epar, ast.literal_eval(med_dict[eu_n])) for eu_n in med_dict)
    else:
        for eu_n in med_dict:
            download_medicine_files(eu_n, decisions, annexes, epar, ast.literal_eval(med_dict[eu_n]))