import csv
import json
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd
from joblib import Parallel, delayed
import tqdm

import download
import ec_scraper
import ema_scraper

# TODO: These variables are for debugging, remove in final
# Flag variables to indicate whether the webscraper should fill the .csv files or not
scrape_ec: bool = False
scrape_ema: bool = False            # Requires scrape_ec to have been run at least once
download_files: bool = True         # Download pdfs from the obtained links
parallel_csv_getting: bool = True   # Parallelization is currently broken on Windows. Set to False

# TODO: Logging to monolithic main
tqdm_format_string = "{l_bar}{bar}| {n_fmt}/{total_fmt} "

# Global configuration of the log file
log_handler_console = logging.StreamHandler()
log_handler_file = logging.FileHandler("webscraper.log")

logging.basicConfig(level=logging.INFO, handlers=[log_handler_console, log_handler_file])

# TODO: To __init__? Figure some stuff out
# Local instance of a logger
log = logging.getLogger(__name__)


# Paralleled function for getting the URL codes. They are written to a CSV file
def get_urls_ec(medicine_url, eu_n):
    attempts = 0
    max_attempts = 4
    success = False
    while attempts < max_attempts and not success:
        try:
            # getURLsForPDFAndEMA returns per medicine the urls for the decision and annexes files and for the ema
            # website.
            dec_list, anx_list, ema_list, med_dict = ec_scraper.scrape_medicine_page(medicine_url)
            with open("../data/CSV/decision.csv", 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([eu_n, dec_list])
            with open("../data/CSV/annexes.csv", 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([eu_n, anx_list])
            with open("../data/CSV/ema_urls.csv", 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([eu_n, ema_list])
            with open("../data/CSV/med_dict.csv", 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([eu_n, med_dict])
            success = True
        except Exception:
            attempts += 1
            if attempts == max_attempts:
                log.error(f"FAILED dec/anx/ema url getting for {eu_n}")
                break


def get_urls_ema(medicine, url: str):
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
            with open("../data/CSV/epar.csv", 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([medicine, pdf_url])
            success = True
        except Exception:
            attempts += 1
            if attempts == max_attempts:
                log.error(f"FAILED ema_pdf url getting for {medicine, url}")
                break


def main():
    log.info(f"=== NEW LOG {datetime.today()} ===")

    # Create the data dir.
    # The ' exist_ok' option ensures no errors thrown if this is not the first time the code runs.
    Path("../data/CSV").mkdir(exist_ok=True, parents=True)
    Path("../data/medicines").mkdir(exist_ok=True)

    log.info("TASK SUCCESS on Generating directories")

    medicine_codes = ec_scraper.scrape_medicines_list(
        "https://ec.europa.eu/health/documents/community-register/html/reg_hum_act.htm")

    log.info("TASK SUCCESS on scraping all medicine URLs of EC")

    with Parallel(n_jobs=12) as parallel:
        # TODO: Progressbar needs to be below logging output
        #       https://stackoverflow.com/questions/6847862/how-to-change-the-format-of-logged-messages-temporarily-in-python
        # log_handler_console.setFormatter(logging.Formatter("\r%(message)s"))
        if scrape_ec:
            log.info("TASK START scraping all medicines on the EC website")
            if parallel_csv_getting:
                parallel(
                    delayed(get_urls_ec)(medicine_url, eu_n)
                    for (medicine_url, eu_n)
                    in tqdm.tqdm(medicine_codes, bar_format=tqdm_format_string)
                )
            else:
                for (medicine_url, eu_n) in tqdm.tqdm(medicine_codes, bar_format=tqdm_format_string):
                    get_urls_ec(medicine_url, eu_n)
            log.info("TASK FINISHED EC scrape")

        if scrape_ema:
            log.info("TASK START scraping all individual medicine pages of EMA")
            ema = pd.read_csv('../data/CSV/ema_urls.csv', header=None, index_col=0).squeeze().to_dict()
            if parallel_csv_getting:
                parallel(
                    delayed(get_urls_ema)(url[0], url[1])
                    for url
                    in tqdm.tqdm(ema.items(), bar_format=tqdm_format_string)
                )
            else:
                for url in tqdm.tqdm(ema.items(), bar_format=tqdm_format_string):
                    get_urls_ema(url[0], url[1])
            log.info("TASK FINISHED EMA scrape")

        # TODO: Same TODO as above
        # log_handler_console.setFormatter(logging.Formatter("%(message)s"))

    if download_files:
        download.download_all(parallel_download=True)


# Keep the code locally testable by including this.
# When running this file specifically, the main function will run.
if __name__ == "__main__":
    main()
