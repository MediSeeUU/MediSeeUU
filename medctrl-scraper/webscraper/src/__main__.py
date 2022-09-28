# Entry point of the Python code
# This will run if you run `python3 .` in the directory

from pathlib import Path
from joblib import Parallel, delayed
from time import sleep
import math

# Create the the data dir. 
# The ' exist_ok' option ensures no errors thrown if this is not the first time the code runs.
path_auth_descis = Path("./data/authorisation_decisions")
path_smpcs       = Path("./data/smpcs")
path_epars       = Path("./data/epars")
path_annexes     = Path("./data/annexes")

path_auth_descis.mkdir(parents=True, exist_ok=True)
path_smpcs.mkdir(exist_ok=True)
path_epars.mkdir(exist_ok=True)
path_annexes.mkdir(exist_ok=True)

import ec_scraper

medicine_codes = ec_scraper.scrape_medicine_urls("https://ec.europa.eu/health/documents/community-register/html/reg_hum_act.htm")

#TODO: Fix parallel getting of the URLs, does not work now due to global variables in combination with parallel processes in python.
# decisions = []
# annexes = []
# ema_urls = []

#parallelised function to get all urls for the decision and annex files and urls to the EMA website
# def downloadall(medicine):
#     attempts = 0
#     max_attempts = 4
#     success = False

#     while attempts < max_attempts and not success:
#         try:
#             dec_list, anx_list, ema_list = ec_scraper.getURLsForPDFAndEMA(medicine)
#             decisions.extend(dec_list)
#             annexes.extend(anx_list)
#             ema_urls.extend(ema_list)
#             print(ema_list)
#             success = True
#         except:
#             attempts += 1
#             if attempts == max_attempts:
#                 break

# Parallel(n_jobs=12)(delayed(downloadall)(medicine) for medicine in medicine_codes)


def downloadall(medicine):
    attempts = 0
    max_attempts = 4
    success = False
    while attempts < max_attempts and not success:
        try:
            dec,anx,ema = ec_scraper.getURLsForPDFAndEMA(medicine)
            success = True
        except:
            attempts += 1
            if attempts == max_attempts:
                break

Parallel(n_jobs=12)(delayed(downloadall)(medicine) for medicine in medicine_codes[:10])
#Old, not parallelised function for getting the URL codes
# for medicine in medicine_codes:
#     #getURLsForPDFAndEMA returns per medicine the urls for the decision and annexes files and for the ema website.
#     dec_list, anx_list, ema_list = ec_scraper.getURLsForPDFAndEMA(medicine)
#     decisions.extend(dec_list)
#     annexes.extend(anx_list)
#     ema_urls.extend(ema_urls)

# df = pd.DataFrame(ema_url_list)
# df.to_csv('./test.csv', header=False)


    