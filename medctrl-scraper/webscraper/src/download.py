import ast
import logging
from pathlib import Path

import pandas as pd
import requests
from joblib import Parallel, delayed

import regex as re

log = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log.addHandler(log_handler)


def download_pdf_from_url(url: str, eu_num: str, filename_elements: list[str]):
    downloaded_file = requests.get(url)
    downloaded_file.raise_for_status()
    filename: str = f"{eu_num}_{'_'.join(filename_elements)}.pdf"

    # TODO: Runs this check for every downloaded file. Could be more efficient?
    path_medicine = Path(f"../data/medicines/{eu_num}")
    path_medicine.mkdir(exist_ok=True)
    with open(f"../data/medicines/{eu_num}/{filename}", "wb") as file:
        file.write(downloaded_file.content)
        log.debug(f"DOWNLOADED {filename} for {eu_num}")


# Download pdfs using the dictionaries created from the CSV files
def download_pdfs_ec(eu_num: str, pdf_type: str, pdf_url_dict: dict[str, list[str]], med_dict: dict[str, str]):
    file_counter = 0
    for url in pdf_url_dict[eu_num]:
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type, str(file_counter)]
        download_pdf_from_url(url, eu_num, filename_elements)
        file_counter += 1


def download_pdfs_ema(eu_num: str, epar_dict: dict[str, str], med_dict: dict[str, str]):
    if eu_num in epar_dict:
        url = epar_dict[eu_num]
        pdf_type = re.findall(r"(?<=epar-)(.*)(?=_en)", url)[0]
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type]
        download_pdf_from_url(url, eu_num, filename_elements)
    else:
        log.info(f"no ema documents available for {eu_num}")


# Function for reading the CSV contents back into dictionaries that can be used for downloading.
def read_csv_files():
    dec = pd.read_csv('../data/CSV/decision.csv', header=None, index_col=0, lineterminator='\n', on_bad_lines='skip').squeeze().to_dict()
    anx = pd.read_csv('../data/CSV/annexes.csv', header=None, index_col=0, lineterminator='\n', on_bad_lines='skip').squeeze().to_dict()
    epar = pd.read_csv('../data/CSV/epar.csv', header=None, index_col=0, lineterminator='\n', on_bad_lines='skip').squeeze().to_dict()
    med_dict = pd.read_csv('../data/CSV/med_dict.csv', header=None, index_col=0, encoding="utf-8", on_bad_lines='skip').squeeze().to_dict()
    return dec, anx, epar, med_dict


# TODO: Add a new function in a way that that function gets a medicine and downloads all files for that medicine.
def download_medicine_files(eu_n: str, dec: dict[str, list[str]], anx: dict[str, list[str]], epar: dict[str, str], med_info: dict[str, str]):
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
def download_all(parallel_download: bool):
    # Store the result of the csv converting into dictionaries
    decisions, annexes, epar, med_dict = read_csv_files()
    log.info("TASK START downloading pdf files from fetched urls from EC and EMA")
    if parallel_download:
        with Parallel(n_jobs=12) as parallel:
            # Download the decision files, parallel
            parallel(
                delayed(download_medicine_files)(eu_n, decisions, annexes, epar, ast.literal_eval(med_dict[eu_n]))
                for eu_n
                in med_dict
            )

    else:
        for eu_n in med_dict:
            download_medicine_files(eu_n, decisions, annexes, epar, ast.literal_eval(med_dict[eu_n]))
    log.info("TASK FINISHED downloading pdf files")
