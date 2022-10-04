import pandas as pd
from joblib import Parallel, delayed
import requests
import regex as re


import sys
import os


# individual pdf download function
def download_pdf_from_url(med_id: str, url: str, pdf_type: str):
    downloaded_file = requests.get(url)
    dec_id = re.findall(rf"(?<={pdf_type}_)\d+", url)[0]
    if pdf_type == "dec":
        with open(f"../data/authorisation_decisions/{med_id}_dec_{dec_id}.pdf", "wb") as file:
            file.write(downloaded_file.content)
            # print(f"  Downloaded {dec_id} decision")
    elif pdf_type == "anx":
        with open(f"../data/annexes/{med_id}_anx_{dec_id}.pdf", "wb") as file:
            file.write(downloaded_file.content)
            # print(f"  Downloaded {dec_id} annex")


def download_epar_from_url(med_id: str, url:str):
    downloaded_file = requests.get(url)
    epar_type = re.findall(r"(?<=epar-)\w+", url)[0]
    if epar_type == "public":
        with open(f"../data/epars/{med_id}_epar.pdf", "wb") as file:
            print(f"download public assessment report from {med_id}")
            file.write(downloaded_file.content)
    elif epar_type == "scientific":
        with open(f"../data/epars/{med_id}_scientific_discussion.pdf", "wb") as file:
            print(f"download scientific discussion from {med_id}")
            file.write(downloaded_file.content)
    elif epar_type == "procedural":
        with open(f"../data/epars/{med_id}_procedural_steps.pdf", "wb") as file:
            print(f"download procedural steps from {med_id}")
            file.write(downloaded_file.content)


# Download pdfs using the dictionaries created from the CSV files
def download_pdfs(med_id, pdf_type, type_dict):
    attempts = 0
    max_attempts = 4
    success = False
    while attempts < max_attempts and not success:
        try:
            for url in list(type_dict[med_id].strip("[]").split(", ")):  # parse csv input
                if pdf_type == "epar":
                    download_epar_from_url(med_id, url)
                else:
                    download_pdf_from_url(med_id, url[1:-1], pdf_type)
            success = True
        except Exception:
            attempts += 1
            if attempts == max_attempts:
                break


# Function for reading the CSV contents back into dictionaries that can be used for downloading.
def read_csv_files():
    dec = pd.read_csv('../data/CSV/decision.csv', header=None, index_col=0, squeeze=True).to_dict()
    anx = pd.read_csv('../data/CSV/annexes.csv', header=None, index_col=0, squeeze=True).to_dict()
    epar = pd.read_csv('../data/CSV/epar.csv', header=None, index_col=0, squeeze=True).to_dict()
    return dec, anx, epar


def run_parallel():
    # Store the result of the csv converting into dictionaries
    decisions, annexes, epar = read_csv_files()
    # Download the decision files, parallel
    Parallel(n_jobs=12)(delayed(download_pdfs)(medicine, "dec", decisions) for medicine in decisions)
    print("Done with decisions")
    # Download the annexes files, parallel
    Parallel(n_jobs=12)(delayed(download_pdfs)(medicine, "anx", annexes) for medicine in annexes)
    print("Done with Annexes")
    # Download the epar files, parallel
    Parallel(n_jobs=12)(delayed(download_pdfs)(medicine, "epar", epar) for medicine in epar)
    print("Done with epars")

