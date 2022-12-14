import json
import logging
import os
from datetime import datetime, date
from itertools import repeat
from pathlib import Path

import regex as re
import requests
import tqdm
import tqdm.contrib.concurrent as tqdm_concurrent
import tqdm.contrib.logging as tqdm_logging

import scraping.utilities.definitions.attributes as attr
import scraping.utilities.log.log_tools as log_tools
from scraping.utilities.web import web_utils as utils, json_helper

log = logging.getLogger("web_scraper.download")


def get_date_from_url(url: str) -> dict[str, str]:
    """
    Retrieves the date from a file (for filedates.json) based on an url. If no date in the url is found, the scrape date
    is used.

    Args:
        url (str): the url where the date should be retrieved from

    Returns:
        (dict[str, str]): A tuple containing the url, the date of the url and the datetime of the scrape
    """
    file_date = datetime.now()
    url_date = re.findall(r"\d{8}", url)
    if url_date:
        url_date = url_date[0]
        if url_date[:2] == "19" or url_date[:2] == "20":
            file_date = datetime.strptime(url_date, '%Y%m%d')
    return {
        attr.file_date_pdf_link: url,
        attr.file_date_pdf_date: str(file_date.date()),
        attr.file_date_pdf_scrape_date: str(date.today())
    }


def save_new_eu_numbers(data_path: str):
    """
    Writes EU numbers of medicines that contain new files to f"{data_path}/eu_numbers.json"

    Args:
        data_path (str): The path to the data folder
    """
    # Get all logging lines as list after latest "NEW LOG"
    log_path = log_tools.get_log_path("logging_web_scraper.log", data_path)
    if os.path.exists(log_path):
        with open(log_path, 'r') as log_file:
            full_log = log_file.read().split("=== NEW LOG ")[-1].split("\n")

        # Only get "New medicine: " lines
        filtered = filter(lambda line: "New medicine: " in line, full_log)

        # Get and write new EU numbers
        eu_numbers = list(map(lambda line: line.split(" ")[2], list(filtered)))
        eu_numbers_path = ""
        eu_numbers_base_path = f"{data_path}/{date.today()}_eu_numbers"

        file_exists = True
        i = 0
        while file_exists:
            eu_numbers_path = f"{eu_numbers_base_path}_{i}.json"
            i += 1
            file_exists = os.path.exists(eu_numbers_path)

        with open(eu_numbers_path, 'w') as outfile:
            json.dump(eu_numbers, outfile)


@utils.exception_retry(logging_instance=log)
def download_pdf_from_url(url: str, medicine_identifier: str, filename_elements: list[str], target_path: str,
                          attr_dict: dict[str, str],
                          overwrite: bool = False):
    """
    Downloads a PDF file given an url. It also gives the file a specific name based on the input.
    The file will be downloaded to the corresponding EU number folder.

    Args:
        url (str): the url towards the page where the pdf file is found
        medicine_identifier (str): the medicine identifier of the medicine where the pdf belongs to, also used to locate
            correct folder
        filename_elements (list[str]): list containing the filename elements: human/orphan, active/withdrawn, pdf type
            and file_index
        target_path (str): the path where the pdf should be downloaded to
        attr_dict (dict[str, dict]): dictionary containing the webdata for every medicine.
        overwrite (bool): if true, files will be downloaded again if they exist
    """
    filename: str = f"{medicine_identifier}_{'_'.join(filename_elements)}.pdf"
    if not attr_dict:
        log.error("No webdata.json dictionary found.")
    elif attr.filedates_web not in attr_dict:
        log.warning(f"No key {attr.filedates_web} in the webdata.json file: {attr_dict}.")
    else:
        attr_dict[attr.filedates_web][filename] = get_date_from_url(url)

    if not overwrite:
        filepath = Path(f"{target_path}/{filename}")
        if os.path.exists(filepath):
            return

    # Adds eu_num to set of EU_numbers that contain newly downloaded files
    log.info(f"New medicine: {medicine_identifier}")
    downloaded_file = requests.get(url)
    if downloaded_file.status_code != 200:
        data_path = target_path.split("active_withdrawn")[0]
        log_path = log_tools.get_log_path("failed.txt", data_path)
        with open(log_path, "a") as f:
            f.write(f"{filename}@{url}@{downloaded_file.status_code}\n")
            return

    Path(f"{target_path}").mkdir(exist_ok=True)
    with open(f"{target_path}/{filename}", "wb") as file:
        file.write(downloaded_file.content)
        log.debug(f"DOWNLOADED {filename} for {medicine_identifier}")


# Download pdfs using the dictionaries created from the json file
def download_pdfs_ec(medicine_identifier: str, pdf_type: str, pdf_urls: list[str], med_dict: dict[str, str],
                     target_path: str,
                     urls_dict: json_helper.JsonHelper, overwrite: bool = False):
    """
    Downloads the pdfs of the EC website files for a specific medicine and a specific file type (decision or annex)
    It evaluates the string in the pdf_urls_dict to a list of urls which then can be used for downloading with the
    download_pdf_from_url function.
    The filename_elements used for structuring the filename are also specified in this function.

    Args:
        medicine_identifier (str):
            The EU number of the medicine where the files should be downloaded for.
        pdf_type (str):
            The type of pdf: decision or annex
        pdf_urls (list[str]):
            The list containing the urls to the pdf files.
        med_dict (dict[str,str]):
            The dictionary containing the attributes of the medicine. Used for structuring the filename
        target_path (str):
            The path to the data folder
        urls_dict (json_helper.JsonHelper): the dictionary containing all the urls of a specific medicine
        overwrite (bool): If true overwrites the current files in the medicine folder
    """
    file_counter = 0
    auth_index = int(med_dict[attr.authorisation_row])
    if len(pdf_urls) > 0:
        for url in pdf_urls[auth_index:]:
            filename_elements = [med_dict[attr.orphan_status], pdf_type, str(file_counter)]
            download_pdf_from_url(url, medicine_identifier, filename_elements, target_path, med_dict)
            file_counter += 1

        file_counter = -auth_index
        for url in pdf_urls[:auth_index]:
            filename_elements = [med_dict[attr.orphan_status], pdf_type, str(file_counter)]
            download_pdf_from_url(url, medicine_identifier, filename_elements, target_path, med_dict,
                                  overwrite)
            file_counter += 1

    if pdf_type == "anx":
        overwrite_dict: json = {
            medicine_identifier: {
                attr.overwrite_ec_files: "False"
            }
        }
        urls_dict.add_to_dict(overwrite_dict)


def download_pdfs_ema(eu_num: str, pdf_type: str, pdf_url: str, med_dict: dict[str, str],
                      target_path: str,
                      overwrite: bool = False):
    """
    Downloads the pdfs of the EMA website files for a specific medicine.
    It gets the url from the epar dictionary which is used for downloading with the download_pdf_from_url function.
    The filename_elements used for structuring the filename are also specified in this function.

    Args:
        eu_num (str): The EU number of the medicine where the files should be downloaded for.
        pdf_type (str): The type of pdf. epar, omar or odwar
        pdf_url (str) The url to the pdf file
        med_dict (dict[str,str]): The dictionary containing the attributes of the medicine.
            Used for structuring the filename
        target_path (str):
            The path to the data folder
        overwrite (bool): If true overwrites the current files in the medicine folder
    """
    if pdf_url == "":
        log.debug(f"no {pdf_type} available for {eu_num}")
        return

    if pdf_type == "epar":
        try:
            pdf_type = re.findall(r"(?<=epar-)(.*)(?=_en)", pdf_url)[0]
        except IndexError:
            log.warning(f"no filetype found for {pdf_url}")

    filename_elements = [med_dict[attr.orphan_status], pdf_type]
    download_pdf_from_url(pdf_url, eu_num, filename_elements, target_path, med_dict, overwrite)


def download_medicine_files(medicine_identifier: str, url_dict: dict[str, list[str] | str],
                            urls_json: json_helper.JsonHelper, data_path: str):
    """
    Downloads all the pdf files that belong to a medicine.
    Logs successful downloads and also logs if not all files could be downloaded for a specific medicine.

    Args:
        medicine_identifier (str): The EU number of the medicine where we want to download the files of
        url_dict (dict[str, list[str] | str]): the dictionary containing all the urls of a specific medicine
        urls_json (json_helper.JsonHelper): The dictionary containing the urls of all medicine files
        data_path (str): The path to the data folder
    """
    # Based on whether the medicine is refused, set the data path where the files need to be downloaded
    if "REFUSED" in medicine_identifier:
        target_path = f"{data_path}/refused/{medicine_identifier}"
    else:
        target_path: str = f"{data_path}/active_withdrawn/{medicine_identifier}"

    # Gets the attribute dictionary for a medicine
    attr_dict = (json_helper.JsonHelper(path=f"{target_path}/{medicine_identifier}_webdata.json")).load_json()

    if attr.filedates_web not in attr_dict.keys():
        attr_dict[attr.filedates_web] = {}

    download_list_ec = [("dec", attr.aut_url), ("anx", attr.smpc_url)]
    for (filetype, key) in download_list_ec:
        if key not in url_dict.keys():
            log.error(f"Key {key} not in keys of url_dict with identifier {medicine_identifier}. url_dict: {url_dict}")
        download_pdfs_ec(medicine_identifier, filetype, url_dict[key], attr_dict, target_path, urls_json,
                         url_dict.get(attr.overwrite_ec_files, "True") == "True")

    download_list_ema = [('epar', attr.epar_url), ('omar', attr.omar_url), ("odwar", attr.odwar_url)]
    for (filetype, key) in download_list_ema:
        if key not in url_dict.keys():
            log.error(f"Key {key} not in keys of url_dict with identifier {medicine_identifier}. "
                      f"Did you run EMA scraper? url_dict: {url_dict}")
        else:
            download_pdfs_ema(medicine_identifier, filetype, url_dict[key], attr_dict, target_path)
    if attr.other_ema_urls not in url_dict.keys():
        log.error(f"Key {attr.other_ema_urls} not in keys of url_dict with identifier {medicine_identifier}."
                  f"Did you run EMA scraper? url_dict: {url_dict}")
    else:
        for url, filetype in url_dict[attr.other_ema_urls]:
            download_pdfs_ema(medicine_identifier, filetype, url, attr_dict, target_path)

    with open(f"{target_path}/{medicine_identifier}_webdata.json", 'w') as f:
        json.dump(attr_dict, f, indent=4)

    log.info(f"Finished download for {medicine_identifier}")


@utils.exception_retry(logging_instance=log)
def download_annex10_files(data_filepath: str, urls_dict: json_helper.JsonHelper):
    """
    Downloads all the Annex 10 files from the EC website

    Args:
        data_filepath (str): Path to the data folder
        urls_dict: The dictionary containing the URLs of the Annex 10 files.
    """
    target_path = f"{data_filepath}/annex_10"

    for year, url_dict in tqdm.tqdm(urls_dict.local_dict.items()):
        url: str = url_dict[attr.annex10_url]
        downloaded_file = requests.get(url)

        # TODO: Refactor this function and download_pdfs_from_url, so that code is not duplicated.
        if downloaded_file.status_code != 200:
            log_path = log_tools.get_log_path("failed.txt", data_filepath)
            with open(log_path, "a") as f:
                f.write(f"annex10_{year}@{url}@{downloaded_file.status_code}\n")
                return

        Path(f"{target_path}").mkdir(exist_ok=True)
        with open(f"{target_path}/annex10_{year}.xlsx", "wb") as file:
            file.write(downloaded_file.content)
            log.debug(f"DOWNLOADED Annex 10 for {year}")


@utils.exception_retry(logging_instance=log)
def download_ema_excel_file(data_filepath: str, urls_dict: json_helper.JsonHelper):
    """
    Downloads the EMA EPAR Excel from the EMA website

    Args:
        data_filepath: Path to the data folder.
        urls_dict: The dictionary containing the URL of the EMA Excel file.
    """
    target_path: str = f"{data_filepath}/ema_excel"
    url: str = urls_dict.load_json().get("url")
    downloaded_file = requests.get(url)

    # TODO: Refactor this function and download_pdfs_from_url, so that code is not duplicated.
    if downloaded_file.status_code != 200:
        log_path = log_tools.get_log_path("failed.txt", data_filepath)
        with open(log_path, "a") as f:
            f.write(f"ema_excel@{url}@{downloaded_file.status_code}\n")
            return

    Path(f"{target_path}").mkdir(exist_ok=True)
    with open(f"{target_path}/ema_excel.xlsx", "wb") as file:
        file.write(downloaded_file.content)
        log.debug(f"DOWNLOADED EMA Excel")


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
                                       repeat(urls_dict),
                                       repeat(data_filepath), max_workers=12)

        else:
            for eu_n, urls_eu_n_dict in tqdm.tqdm(urls_dict.local_dict.items()):
                download_medicine_files(eu_n, urls_eu_n_dict, urls_dict, data_filepath)

    save_new_eu_numbers(data_filepath)

    log.info("TASK FINISHED downloading PDF files")
