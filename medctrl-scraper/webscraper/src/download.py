import ast
import logging
from pathlib import Path

import pandas as pd
import requests
from joblib import Parallel, delayed

log = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log.addHandler(log_handler)


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
# TODO: pdf_type_dict value is dict[str, str], but should be dict[str, [str]]
def download_pdfs_ec(eu_num: str, pdf_type: str, pdf_url_dict: dict[str, str], med_dict: dict[str, str]):
    attempts = 0
    max_attempts = 4
    success = False
    # TODO: Rework with new download method
    # TODO: Add file_number and pdf_type to filenames list.
    while attempts < max_attempts and not success:
        try:
            file_counter = 0
            for url in ast.literal_eval(pdf_url_dict[eu_num]):
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

    with Parallel(n_jobs=12) as parallel:
        # Download the decision files, parallel
        log.info("TASK START downloading Decisions from fetched urls from EC")
        parallel(
            delayed(download_pdfs_ec)(eu_n, "dec", decisions, ast.literal_eval(med_dict[eu_n]))
            for eu_n
            in decisions
        )
        log.info("TASK FINISHED downloading Decisions EC")

        # Download the annexes files, parallel
        log.info("TASK START downloading Annexes from fetched urls from EC")
        parallel(
            delayed(download_pdfs_ec)(eu_n, "anx", annexes, ast.literal_eval(med_dict[eu_n]))
            for eu_n
            in annexes
        )
        log.info("TASK FINISHED downloading Annexes EC")

        """
        # TODO: download_pdf has been refactored, rewrite needed.
        # Download the epar files, parallel
        log.info("TASK START downloading EPARs from fetched urls from EMA")
        parallel(
            delayed(download_pdf)(medicine, "epar", epar) 
            for medicine 
            in epar
        )
        log.info("TASK FINISHED downloading EPARs EMA")
        """
