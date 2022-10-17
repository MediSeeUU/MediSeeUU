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
    attempts = 0
    max_attempts = 4
    success = False
    # TODO: Rework with new download method
    # TODO: Add file_number and pdf_type to filenames list.
    while attempts < max_attempts and not success:
        try:
            file_counter = 0
            for url in ast.literal_eval(pdf_type_dict[eu_num]):
                filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type, str(file_counter)]
                download_pdf_from_url(url, eu_num, filename_elements)
                file_counter += 1
            success = True
        except Exception:
            attempts += 1


# Function for reading the CSV contents back into dictionaries that can be used for downloading.
def read_csv_files():
    dec = pd.read_csv('../data/CSV/decision.csv', header=None, index_col=0).squeeze().to_dict()
    anx = pd.read_csv('../data/CSV/annexes.csv', header=None, index_col=0).squeeze().to_dict()
    epar = pd.read_csv('../data/CSV/epar.csv', header=None, index_col=0).squeeze().to_dict()
    med_dict = pd.read_csv('../data/CSV/med_dict.csv', header=None, index_col=0).squeeze().to_dict()
    return dec, anx, epar, med_dict


# TODO: Add a new function in a way that that function gets a medicine and downloads all files for that medicine.


# TODO: Fix downloading for epar files
def run_parallel():
    # Store the result of the csv converting into dictionaries
    decisions, annexes, epar, med_dict = read_csv_files()
    # Download the decision files, parallel
    Parallel(n_jobs=12)(delayed(download_pdfs_ec)(eu_n, "dec", decisions, ast.literal_eval(med_dict[eu_n])) for eu_n in decisions)
    log.info("Done with decisions")
    # Download the annexes files, parallel
    Parallel(n_jobs=12)(delayed(download_pdfs_ec)(eu_n, "anx", annexes, ast.literal_eval(med_dict[eu_n])) for eu_n in annexes)
    log.info("Done with Annexes")
    # # Download the epar files, parallel
    # Parallel(n_jobs=12)(delayed(download_pdfs)(medicine, "epar", epar) for medicine in epar)
    # print("Done with epars")
