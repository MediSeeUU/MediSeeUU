# Entry point of the Python code
# This will run if you run `python3 .` in the directory

import csv
import json
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd
from joblib import Parallel, delayed

import download
import ec_scraper
import ema_scraper

# Global configuration of the log file
logging.basicConfig(filename='webscraper.log', level=logging.INFO)

# Local instance of a logger
log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())

log.info(f"=== NEW LOG {datetime.today()} ===")

# Create the data dir.
# The ' exist_ok' option ensures no errors thrown if this is not the first time the code runs.
path_csv = Path("../data/CSV")
path_medicines = Path("../data/medicines")

path_csv.mkdir(exist_ok=True, parents=True)
path_medicines.mkdir(exist_ok=True)

log.info("SUCCESS on Generating directories")

medicine_codes = ec_scraper.scrape_medicines_list(
    "https://ec.europa.eu/health/documents/community-register/html/reg_hum_act.htm")

log.info("SUCCESS on scraping all medicine URLs of EC")


# Paralleled function for getting the URL codes. They are written to a CSV file
def get_urls_ec(medicine, eu_n):
    attempts = 0
    max_attempts = 4
    success = False
    while attempts < max_attempts and not success:
        try:
            # getURLsForPDFAndEMA returns per medicine the urls for the decision and annexes files and for the ema
            # website.
            dec_list, anx_list, ema_list = ec_scraper.scrape_medicine_page(medicine)
            with open("../data/CSV/decision.csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow([eu_n, medicine, dec_list])
            with open("../data/CSV/annexes.csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow([eu_n, medicine, anx_list])
            with open("../data/CSV/ema_urls.csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow([eu_n, medicine, ema_list])
            success = True
        except Exception:
            attempts += 1
            if attempts == max_attempts:
                print(f"failed dec/anx/ema url getting for {medicine, eu_n}")
                break


def get_urls_ema(key, url: str):
    eu_n, medicine = key
    attempts = 0
    max_attempts = 4
    success = False
    while attempts < max_attempts and not success:
        try:
            if url != "[]":
                url = json.loads(url.replace('\'', '"'))[0]
            else:
                url = ''
            pdf_url = ema_scraper.pdf_links_from_url(url)
            with open("../data/CSV/epar.csv", 'a') as f:
                writer = csv.writer(f)
                writer.writerow([eu_n, medicine, pdf_url])
            success = True
        except Exception:
            attempts += 1
            if attempts == max_attempts:
                log.error(f"failed ema_pdf url getting for {eu_n, url}")
                # print(f"failed ema_pdf url getting for {medicine, url}")
                break


# NOTE: Use the line of code below to fill all the CSV files.
# If you have a complete CSV file, this line of code below is not needed.
Parallel(n_jobs=12)(delayed(get_urls_ec)(medicine, eu_n) for medicine, eu_n in medicine_codes)
log.info("SUCCESS on scraping all individual medicine pages of EC")

# NOTE: Use the lines of code below to fill epar.csv
# epar.csv will contain the links to the epar pdfs.
ema = pd.read_csv('../data/CSV/ema_urls.csv', header=None, index_col=(0, 1)).squeeze().to_dict()

Parallel(n_jobs=12)(delayed(get_urls_ema)(url[0], url[1]) for url in ema.items())
log.info("SUCCESS on scraping all individual medicine pages of EMA")


# NOTE: Use the line of code below to download all files.
# download.run_parallel()
