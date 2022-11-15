import logging
from pathlib import Path

import regex as re
import requests
import tqdm
import tqdm.contrib.concurrent as tqdm_concurrent
import tqdm.contrib.logging as tqdm_logging
import os

from scraping.web_scraper import json_helper
from scraping.web_scraper import utils

log = logging.getLogger("webscraper.download")


@utils.exception_retry(logging_instance=log)
def download_pdf_from_url(url: str, eu_num: str, filename_elements: list[str], data_path: str, overwrite: bool = False):
    """
    Downloads a PDF file given an url. It also gives the file a specific name based on the input.
    The file will be downloaded to the corresponding EU number folder.

    Args:
        url (str):
            the url towards the page where the pdf file is found
        eu_num (str):
            the EU number of the medicine where the pdf belongs to, also used to locate correct folder
        filename_elements (list[str]):
            list containing the filename elements: human/orphan, active/withdrawn, pdf type and file_index
        data_path (str):
            The path to the data folder
        overwrite (bool): if true, files will be downloaded again if they exist
    """

    filename: str = f"{eu_num}_{'_'.join(filename_elements)}.pdf"
    if not overwrite:
        filepath = Path(f"{data_path}/{eu_num}/{filename}")
        if os.path.exists(filepath):
            return

    downloaded_file = requests.get(url)
    if downloaded_file.status_code != 200:
        with open(f"failed.txt", "a") as f:
            f.write(f"{filename}@{url}@{downloaded_file.status_code}\n")
            return
    # TODO: Runs this check for every downloaded file. Could be more efficient?
    path_medicine = Path(f"{data_path}/{eu_num}")
    path_medicine.mkdir(exist_ok=True)
    with open(f"{data_path}/{eu_num}/{filename}", "wb") as file:
        file.write(downloaded_file.content)
        log.debug(f"DOWNLOADED {filename} for {eu_num}")


# Download pdfs using the dictionaries created from the json file
def download_pdfs_ec(eu_num: str, pdf_type: str, pdf_urls: list[str], med_dict: dict[str, str], data_path: str):
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
        pdf_urls (list[str]):
            The list containing the urls to the pdf files.
        med_dict (dict[str,str]):
            The dictionary containing the attributes of the medicine. Used for structuring the filename
        data_path (str):
            The path to the data folder
    """
    file_counter = 0
    for url in pdf_urls:
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type, str(file_counter)]
        download_pdf_from_url(url, eu_num, filename_elements, data_path)
        file_counter += 1


def download_pdfs_ema(eu_num: str, pdf_type: str, pdf_url: str, med_dict: dict[str, str], data_path: str):
    """
    Downloads the pdfs of the EMA website files for a specific medicine.
    It gets the url from the epar dictionary which is used for downloading with the download_pdf_from_url function.
    The filename_elements used for structuring the filename are also specified in this function.

    Args:
        eu_num (str): The EU number of the medicine where the files should be downloaded for.
        pdf_type (str): The type of pdf, epar or omar
        pdf_url (str) The url to the pdf file
        med_dict (dict[str,str]): The dictionary containing the attributes of the medicine.
            Used for structuring the filename
        data_path (str):
            The path to the data folder
    """
    if pdf_url == '':
        log.info(f"no {pdf_type} available for {eu_num}")
        return
    if pdf_type != 'omar':
        try:
            pdf_type = re.findall(r"(?<=epar-)(.*)(?=_en)", pdf_url)[0]
        except IndexError:
            log.warning(f"no filetype found for {pdf_url}")
    filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type]
    download_pdf_from_url(pdf_url, eu_num, filename_elements, data_path)


def download_medicine_files(eu_n: str, url_dict: dict[str, list[str] | str], data_path: str = "../data"):
    """
    Downloads all the pdf files that belong to a medicine.
    Logs successful downloads and also logs if not all files could be downloaded for a specific medicine.

    Args:
        eu_n (str): The EU number of the medicine where we want to download the files of
        url_dict (dict[str, list[str] | str]): the dictionary containing all the urls of a specific medicine
        data_path (str): The path to the data folder
    """
    if "web_scraper" in os.getcwd():
        data_path = "../../data"
    # print(f"{data_path}/{eu_n}/{eu_n}_webdata.json")
    attr_dict = (json_helper.JsonHelper(path=f"{data_path}/{eu_n}/{eu_n}_webdata.json")).load_json()
    if "aut_url" in url_dict.keys():
        download_pdfs_ec(eu_n, "dec", url_dict["aut_url"], attr_dict, data_path)
    if "smpc_url" in url_dict.keys():
        download_pdfs_ec(eu_n, "anx", url_dict["smpc_url"], attr_dict, data_path)
    if "epar_url" in url_dict.keys():
        download_pdfs_ema(eu_n, "epar", url_dict["epar_url"], attr_dict, data_path)
    if "omar_url" in url_dict.keys():
        download_pdfs_ema(eu_n, "omar", url_dict["omar_url"], attr_dict, data_path)
    log.info(f"Finished download for {eu_n}")


def download_all(data_filepath: str, urls_dict: json_helper.JsonHelper, parallel_download: bool):
    """
    Downloads all files for all medicines. Can be done parallel or sequential.
    First it reads the CSV files, and then calls download_medicine_files function for all medicines.

    Args:
        data_filepath (str): the path to the data folder
        urls_dict (json_helper.JsonHelper): The dictionary containing the urls of all medicine files
        parallel_download (bool): If this boolean is set to True, the files will be downloaded parallel
    """
    with tqdm_logging.logging_redirect_tqdm():
        if parallel_download:
            tqdm_concurrent.thread_map(download_medicine_files,
                                       urls_dict.local_dict.keys(),
                                       urls_dict.local_dict.values(), max_workers=12)

        else:
            for eu_n, urls_eu_n_dict in tqdm.tqdm(urls_dict.local_dict.items()):
                download_medicine_files(eu_n, urls_eu_n_dict, data_filepath)
