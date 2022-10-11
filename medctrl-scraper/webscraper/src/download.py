import pandas as pd
from joblib import Parallel, delayed
import requests
import regex as re
from pathlib import Path

import sys
import os
import logging

from requests import Response

log = logging.getLogger(__name__)


def download_pdf_from_url(url: str, eu_num: str, filename_elements: list[str]):
    downloaded_file = requests.get(url)
    filename: str = '_'.join(filename_elements) + ".pdf"

    # TODO: Runs this check for every downloaded file. Could be more efficient?
    path_medicine = Path(f"../data/medicines/{eu_num}")
    path_medicine.mkdir(exist_ok=True)

    with open(f"../data/medicines/{eu_num}/{eu_num}_{filename}") as file:
        file.write(downloaded_file.content)
        log.debug(f"DOWNLOADED {filename} for {eu_num}")


# Download pdfs using the dictionaries created from the CSV files
def download_pdfs(eu_n: str, pdf_type: str, type_dict: str, filenames):
    attempts = 0
    max_attempts = 4
    success = False
    # TODO: Rework with new download method
    # TODO: Add file_number and pdf_type to filenames list.
    """
    while attempts < max_attempts and not success:
        try:
            for url in list(type_dict[med_id].strip("[]").split(", ")):  # parse csv input
                if pdf_type == "epar":
                    download_epar_from_ema(med_id, url)
                else:
                    download_pdf_from_ec(url[1:-1], med_id, pdf_type)
            success = True
        except Exception:
            attempts += 1
    """


# Function for reading the CSV contents back into dictionaries that can be used for downloading.
def read_csv_files():
    dec = pd.read_csv('../data/CSV/decision.csv', header=None, index_col=0).squeeze().to_dict()
    anx = pd.read_csv('../data/CSV/annexes.csv', header=None, index_col=0).squeeze().to_dict()
    epar = pd.read_csv('../data/CSV/epar.csv', header=None, index_col=0).squeeze().to_dict()
    fnames = pd.read_csv('../data/CSV/filenames.csv', header=None, index_col=0).squeeze().to_dict()
    return dec, anx, epar, fnames

#dec, anx, epar, fnames = read_csv_files()


def run_parallel():
    # Store the result of the csv converting into dictionaries
    decisions, annexes, epar, fnames = read_csv_files()
    # Download the decision files, parallel
    Parallel(n_jobs=12)(delayed(download_pdfs)(medicine, "dec", decisions, fnames[medicine]) for medicine in decisions)
    print("Done with decisions")
    # Download the annexes files, parallel
    Parallel(n_jobs=12)(delayed(download_pdfs)(medicine, "anx", annexes) for medicine in annexes)
    print("Done with Annexes")
    # Download the epar files, parallel
    Parallel(n_jobs=12)(delayed(download_pdfs)(medicine, "epar", epar) for medicine in epar)
    print("Done with epars")
