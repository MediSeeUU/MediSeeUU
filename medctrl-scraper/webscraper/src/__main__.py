# Entry point of the Python code
# This will run if you run `python3 .` in the directory

import csv
from pathlib import Path

import pandas as pd
from joblib import Parallel, delayed

from . import ec_scraper

# Create the data dir.
# The ' exist_ok' option ensures no errors thrown if this is not the first time the code runs.
path_auth_descis = Path("./data/authorisation_decisions")
path_smpcs = Path("./data/smpcs")
path_epars = Path("./data/epars")
path_annexes = Path("./data/annexes")
path_csv = Path("./data/CSV")

path_auth_descis.mkdir(parents=True, exist_ok=True)
path_smpcs.mkdir(exist_ok=True)
path_epars.mkdir(exist_ok=True)
path_annexes.mkdir(exist_ok=True)
path_csv.mkdir(exist_ok=True)

medicine_codes = ec_scraper.scrape_medicine_urls(
    "https://ec.europa.eu/health/documents/community-register/html/reg_hum_act.htm")


# Paralleled function for getting the URL codes. They are written to a CSV file
def get_urls(medicine):
    attempts = 0
    max_attempts = 4
    success = False
    while attempts < max_attempts and not success:
        try:
            # getURLsForPDFAndEMA returns per medicine the urls for the decision and annexes files and for the ema
            # website.
            dec_list, anx_list, ema_list = ec_scraper.get_urls_for_pdf_and_ema(medicine)
            with open("./data/CSV/decision.csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow([medicine, dec_list])
            with open("./data/CSV/annexes.csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow([medicine, anx_list])
            with open("./data/CSV/ema_urls.csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow([medicine, ema_list])
            success = True
        except Exception:
            attempts += 1
            if attempts == max_attempts:
                break


# NOTE: Use the line of code below to fill all the CSV files.
# If you have complete CSV file, this line of code below is not needed.
# Parallel(n_jobs=12)(delayed(getURLs)(medicine) for medicine in medicine_codes)
print("Done with URL getting")


# Download pdfs using the dictionaries created from the CSV files
def download_pdfs(med_id, pdf_type, type_dict):
    attempts = 0
    max_attempts = 4
    success = False
    while attempts < max_attempts and not success:
        try:
            for url in list(type_dict[med_id].strip("[]").split(", ")):  # parse csv input
                print(url[1:-1])
                ec_scraper.download_pdf_from_url(med_id, url[1:-1], pdf_type)
            success = True
        except Exception:
            attempts += 1
            if attempts == max_attempts:
                break


# Function for reading the CSV contents back into dictionaries that can be used for downloading.
def read_csv_files():
    dec = pd.read_csv('./data/CSV/decision.csv', header=None, index_col=0, squeeze=True).to_dict()
    anx = pd.read_csv('./data/CSV/annexes.csv', header=None, index_col=0, squeeze=True).to_dict()
    ema = pd.read_csv('./data/CSV/ema_urls.csv', header=None, index_col=0, squeeze=True).to_dict()
    return dec, anx, ema


# Store the result of the csv converting into dictionaries
decisions, annexes, ema_urls = read_csv_files()


def run_parallel():
    # Download the decision files, parallel
    Parallel(n_jobs=12)(delayed(download_pdfs)(medicine, "dec", decisions) for medicine in decisions)
    print("Done with decisions")
    # Download the annexes files, parallel
    Parallel(n_jobs=12)(delayed(download_pdfs)(medicine, "anx", annexes) for medicine in annexes)
    print("Done with Annexes")

# run_parallel()
