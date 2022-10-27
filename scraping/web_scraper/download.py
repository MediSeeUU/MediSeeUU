import ast
import logging
import os
from pathlib import Path

import pandas as pd
import requests
from joblib import Parallel, delayed

import regex as re
import os

log = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
log.addHandler(log_handler)

# TODO: make sure the data path is declared somewhere in main.
data_path = '../data'


def download_pdf_from_url(url: str, eu_num: str, filename_elements: list[str]):
    """
    Downloads a pdf file given an url. It also gives the file a specific name based on the input.
    The file will be downloaded to the corresponding EU number folder.

    Args:
        url (str):
            the url towards the page where the pdf file is found
        eu_num (str):
            the EU number of the medicine where the pdf belongs to, also used to locate correct folder
        filename_elements (list[str]):
            list containing the filename elements: human/orphan, active/withdrawn, pdf type and file_index

    Returns:
        None: This function returns nothing.
    """
    downloaded_file = requests.get(url)
    downloaded_file.raise_for_status()
    filename: str = f"{eu_num}_{'_'.join(filename_elements)}.pdf"

    # TODO: Runs this check for every downloaded file. Could be more efficient?
    path_medicine = Path(f"{data_path}/{eu_num}")
    path_medicine.mkdir(exist_ok=True)
    with open(f"{data_path}/{eu_num}/{filename}", "wb") as file:
        file.write(downloaded_file.content)
        log.debug(f"DOWNLOADED {filename} for {eu_num}")


# Download pdfs using the dictionaries created from the CSV files
def download_pdfs_ec(eu_num: str, pdf_type: str, pdf_url_dict: dict[str, str], med_dict: dict[str, str]):
    """
    Downloads the pdfs of the EC website files for a specific medicine and a specific file type (decision or annex)
    It evaluates the string in the pdf_url_dict to a list of urls which then can be used for downloading with the
    download_pdf_from_url function.
    The filename_elements used for structuring the filename are also specified in this function.

    Args:
        eu_num (str):
            The EU number of the medicine where the files should be downloaded for.
        pdf_type (str):
            The type of pdf: decision or annex
        pdf_url_dict (dict[str,str]):
            The dictionary containing the urls to the pdf files.
        med_dict (dict[str,str]):
            The dictionary containing the attributes of the medicine. Used for structuring the filename

    Returns:
        None: This function returns nothing.

    """
    file_counter = 0
    for url in ast.literal_eval(pdf_url_dict[eu_num]):
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type, str(file_counter)]
        download_pdf_from_url(url, eu_num, filename_elements)
        file_counter += 1


def download_pdfs_ema(eu_num: str, epar_dict: dict[str, str], med_dict: dict[str, str]):
    """
    Downloads the pdfs of the EMA website files for a specific medicine.
    It gets the url from the epar dictionary which is used for downloading with the download_pdf_from_url function.
    The filename_elements used for structuring the filename are also specified in this function.

    Args:
        eu_num (str): The EU number of the medicine where the files should be downloaded for.
        epar_dict (dict[str,str]): The dictionary containing the urls to the epar pdf files.
        med_dict (dict[str,str]): The dictionary containing the attributes of the medicine. Used for structuring the filename

    Returns:
        None: This function returns nothing.
    """
    if eu_num in epar_dict:
        url = epar_dict[eu_num]
        pdf_type = re.findall(r"(?<=epar-)(.*)(?=_en)", url)[0]
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type]
        download_pdf_from_url(url, eu_num, filename_elements)
    else:
        log.info(f"no ema documents available for {eu_num}")


# Function for reading the CSV contents back into dictionaries that can be used for downloading.
def read_csv_files():
    """
    Reads the csv files and converts them into dictionaries that can be used for downloading

    Returns:
        (dict[str,str], dict[str,str], dict[str,str], dict[str,str]): This function returns three dictionaries
            with EU number as keys and urls to files as values, and one dictionary with EU number as key and
            an attribute dictionary as value.

    """
    dec = pd.read_csv('web_scraper/CSV/decision.csv', header=None, index_col=0, lineterminator='\n',
                      on_bad_lines='skip').squeeze().to_dict()
    anx = pd.read_csv('web_scraper/CSV/annexes.csv', header=None, index_col=0, lineterminator='\n',
                      on_bad_lines='skip').squeeze().to_dict()
    epar = pd.read_csv('web_scraper/CSV/epar.csv', header=None, index_col=0, lineterminator='\n',
                       on_bad_lines='skip').squeeze().to_dict()
    med_dict = pd.read_csv('web_scraper/CSV/med_dict.csv', header=None, index_col=0, encoding="utf-8",
                           on_bad_lines='skip').squeeze().to_dict()

    return dec, anx, epar, med_dict


# helper function that converts a windows csv file to linux.
def dos2unix(f_in: str):
    """
    Helper function that converts a windows csv file to linux csv files.
    It takes a CSV file, replaces the line endings and writes this to another csv file.
    After this the new csv file will replace the old csv file.

    Args:
        f_in (str): The filepath towards the to-be-converted csv file

    Returns:
        None: This function returns nothing
    """
    with open('web_scraper/CSV/temp.csv', "w") as f_out:
        with open(f_in, "r") as fin:
            for line in fin:
                line = line.replace('\r\n', '\n')
                f_out.write(line)
    os.rename('web_scraper/CSV/temp.csv', f_in)


def download_medicine_files(eu_n: str, dec: dict[str, str], anx: dict[str, str], epar: dict[str, str],
                            med_info: dict[str, str]):
    """
    Downloads all the pdf files that belong to a medicine.
    Logs succesful downloads and also logs if not all files could be downloaded for a specific medicine.

    Args:
        eu_n (str): The EU number of the medicine where we want to download the files of
        dec (dict[str,str]): The dictionary containing the urls of the decisions pdf files
        anx (dict[str,str]): The dictionary containing the urls of the annexes pdf files
        epar (dict[str,str]): The dictionary containing the urls of the EMA website files
        med_info (dict[str,str]): The dictionary containing the attributes of a specific medicine.

    Returns:
        None: This function returns nothing
    """
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
        except:
            attempts += 1
            log.info(f"Failed getting all pdf files for {eu_n}")


def download_all(parallel_download: bool):
    """
    Downloads all files for all medicines. Can be done parallel or sequential.
    First it reads the CSV files, and then calls download_medicine_files function for all medicines.

    Args:
        parallel_download (bool): If this boolean is set to True, the files will be downloaded parallel

    Returns:
        None: This function returns nothing

    """
    # dos2unix('web_scraper/CSV/epar.csv')
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
