from datetime import datetime
import logging
from pathlib import Path

import regex as re
import requests
import tqdm
import tqdm.contrib.concurrent as tqdm_concurrent
import tqdm.contrib.logging as tqdm_logging
from itertools import repeat
import os
import json

from scraping.web_scraper import json_helper
from scraping.web_scraper import utils

log = logging.getLogger("web_scraper.download")


def get_date_from_url(url: str):
    """
    Retrieves the date from a file (for filedates.json) based on an url. If no date in the url is found, the scrape date
    is used.

    Args:
        url: the url where the date should be retrieved from

    Returns:
        A tuple containing the url, the date of the url and the datetime of the scrape
    """
    date = datetime.now()
    url_date = (re.findall(r"\d{8}", url))
    if len(url_date) > 0:
        date = datetime.strptime(url_date[0], '%Y%m%d')
    return tuple((url, date, datetime.now()))


@utils.exception_retry(logging_instance=log)
def download_pdf_from_url(url: str, eu_num: str, filename_elements: list[str], data_path: str,
                          filedate_dict: dict[str, tuple[str, datetime, datetime]],
                          overwrite: bool = False):
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
        filedate_dict (dict[str, tuple[str, datetime, datetime]]):
            dictionary containing the date for every file. in the format {filename : (url, date)}
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

    filedate_dict[filename] = get_date_from_url(url)


# Download pdfs using the dictionaries created from the json file
def download_pdfs_ec(eu_num: str, pdf_type: str, pdf_urls: list[str], med_dict: dict[str, str],
                     filedate_dict: dict[str, tuple[str, datetime, datetime]],
                     data_path: str):
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
        filedate_dict (dict[str, tuple[str, datetime, datetime]]):
            dictionary containing the date for every file. in the format {filename : (url, date)}
        data_path (str):
            The path to the data folder
    """
    file_counter = 0
    if len(pdf_urls) > 0:
        for url in pdf_urls[:-1]:
            filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type, str(file_counter)]
            download_pdf_from_url(url, eu_num, filename_elements, data_path, filedate_dict)
            file_counter += 1
        if med_dict["init_addressed_to_member_states"] == "True":
            file_counter = -1
        filename_elements = [med_dict["orphan_status"], med_dict["status_type"], pdf_type, str(file_counter)]
        download_pdf_from_url(pdf_urls[-1], eu_num, filename_elements, data_path, filedate_dict)


def download_pdfs_ema(eu_num: str, pdf_type: str, pdf_url: str, med_dict: dict[str, str],
                      filedate_dict: dict[str, tuple[str, datetime, datetime]], data_path: str):
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
        filedate_dict (dict[str, tuple[str, datetime, datetime]]):
            dictionary containing the date for every file. in the format {filename : (url, date)}
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
    download_pdf_from_url(pdf_url, eu_num, filename_elements, data_path, filedate_dict)


def download_medicine_files(eu_n: str, url_dict: dict[str, list[str] | str], data_path: str):
    """
    Downloads all the pdf files that belong to a medicine.
    Logs successful downloads and also logs if not all files could be downloaded for a specific medicine.

    Args:
        eu_n (str): The EU number of the medicine where we want to download the files of
        url_dict (dict[str, list[str] | str]): the dictionary containing all the urls of a specific medicine
        data_path (str): The path to the data folder
    """
    attr_dict = (json_helper.JsonHelper(path=f"{data_path}/{eu_n}/{eu_n}_webdata.json")).load_json()
    filedate_dict = {}
    filedates_path = f"{data_path}/{eu_n}/{eu_n}_filedates.json"
    if os.path.exists(filedates_path):
        with open(filedates_path, 'r') as f:
            filedate_dict = json.load(f)
    download_list = [("dec", "aut_url"), ("anx", "smpc_url"), ('epar', "epar_url"), ('omar', "omar_url")]
    for (filetype, key) in download_list:
        if key in url_dict.keys() and filetype in ["dec", "anx"]:
            download_pdfs_ec(eu_n, filetype, url_dict[key], attr_dict, filedate_dict, data_path)
        if key in url_dict.keys() and filetype in ['epar', 'omar']:
            download_pdfs_ema(eu_n, filetype, url_dict[key], attr_dict, filedate_dict, data_path)
    with open(filedates_path, 'w') as f:
        json.dump(filedate_dict, f, indent=4, default=str)
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
                                       urls_dict.local_dict.values(),
                                       repeat(data_filepath), max_workers=12)

        else:
            for eu_n, urls_eu_n_dict in tqdm.tqdm(urls_dict.local_dict.items()):
                download_medicine_files(eu_n, urls_eu_n_dict, data_filepath)
