import datetime
import json
import logging
import multiprocessing
import os.path as path
from os import listdir

import joblib
from tqdm import tqdm

import scraping.pdf_parser.parsed_info_struct as pis
import scraping.utilities.definitions.attributes as attr
from scraping.pdf_parser.parsers import annex_parser
# for main
from scraping.pdf_parser.parsers import dec_parser
from scraping.pdf_parser.parsers import epar_parser
from scraping.pdf_parser.parsers import omar_parser

log = logging.getLogger("pdf_parser")


# Main file to run all parsers
def main(directory: str, parse_all: bool = False):
    """
    given a folder containing medicine folders, parses each folder in parallel

    Args:
        directory: data folder, containing medicine folders
        parse_all: Whether to parse all medicines, regardless of the eu_numbers.json
    """
    log.info(f"=== NEW LOG {datetime.datetime.today()} ===")

    eu_numbers_path = ""
    eu_numbers_base_path = f"{directory}/{datetime.date.today()}_eu_numbers"

    file_exists = True
    i = 0
    while file_exists:
        eu_numbers_path = eu_numbers_base_path + f"_{i}.json"
        i += 1
        file_exists = path.exists(eu_numbers_base_path + f"_{i}.json")

    if path.exists(eu_numbers_path):
        with open(eu_numbers_path) as f:
            eu_numbers = set(json.load(f))
    else:
        eu_numbers = {}
        log.warning(f"No eu_numbers.json file found at location {eu_numbers_path}. Did you run web scraper?")

    meds_dir = f"{directory}/active_withdrawn"

    if parse_all:
        directory_folders = [folder for folder in listdir(meds_dir) if path.isdir(path.join(meds_dir, folder))]
    else:
        # Get medicine folders that have yet to be scraped, so only medicines in the eu_numbers.json file
        directory_folders = [folder for folder in listdir(meds_dir) if path.isdir(path.join(meds_dir, folder)) and
                             (folder in eu_numbers or folder_has_no_pdf_json(meds_dir, folder))]

    # Use all the system's threads to maximize use of all hyper-threads
    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(parse_folder)(path.join(meds_dir, folder), folder) for folder in
        tqdm(directory_folders))
    log.info("Done parsing PDF files!")


# scraping on medicine folder level
def parse_folder(directory: str, folder_name: str):
    """
    Given a folder containing medicines, parse_folder walks creates an XML file for each PDF when it doesn't exist.
        After this, a parser for each pdf/xml file is called,
        writing a json file containing the scraped attributes to the folder.

    Args:
        directory (str): location of folder to parse
        folder_name (st): name of medicine folder to parse
    """

    # struct that contains all scraped attributes dicts as well as eu_number and date of parsing
    medicine_struct = pis.ParsedInfoStruct(folder_name)

    # update list of files and filter out relevant files for each parser
    annex_files, decision_files, epar_files, omar_files, odwar_files = get_files(directory)

    # call scrapers on correct files and update medicine struct
    medicine_struct = run_scrapers(directory, annex_files, decision_files, epar_files, omar_files, odwar_files,
                                   medicine_struct)

    # dump json result to medicine folder directory
    json_file = open(path.join(directory, folder_name) + "_pdf_parser.json", "w")
    medicine_struct_json = json.dumps(pis.asdict(medicine_struct), default=datetime_serializer)
    json_file.write(medicine_struct_json)
    json_file.close()


def get_files(directory: str) -> (list[str], list[str], list[str], list[str], list[str]):
    """
    Get all PDF and XML files per PDF type

    Args:
        directory (str): Location of the data folder

    Returns:
        (list[str], list[str], list[str], list[str], list[str]): List of PDF file names for each of the 5 PDF types
    """
    directory_files = [file for file in listdir(directory) if path.isfile(path.join(directory, file))
                       and "other" not in file]
    decision_files = [file for file in directory_files if "dec" in file and ".xml" not in file]
    annex_files = [path.join(directory, file) for file in directory_files if "anx" in file and ".xml" in file]
    epar_files = [file for file in directory_files if
                  ("public-assessment-report" in file or "procedural-steps-taken" in file or "epar" in file)
                  and ".xml" in file]
    omar_files = [path.join(directory, file) for file in directory_files if
                  ("omar" in file or "orphan" in file) and ".xml" in file]
    odwar_files = [path.join(directory, file) for file in directory_files if
                   "odwar" in file and ".xml" in file]
    return annex_files, decision_files, epar_files, omar_files, odwar_files


def run_scrapers(directory: str, annex_files: list[str], decision_files: list[str], epar_files: list[str],
                 omar_files: list[str], odwar_files: list[str], medicine_struct: pis.ParsedInfoStruct):
    """
    Scraping all XML or PDF files and updating medicine_struct with the scraped attributes

    Args:
        directory (list[str]): directory of folder containing the files
        annex_files (list[str]): list of file names for annex files
        decision_files (list[str]): list of file names for decisions files
        epar_files (list[str]): list of file names for epar files
        omar_files (list[str]): list of file names for omar files
        odwar_files (list[str]): list of file names for odwar files
        medicine_struct (pis.ParsedInfoStruct): struct to add parsed attributes to

    Returns:
        pis.ParsedInfoStruct: Medicine structure containing scraped attributes
    """
    log.info("Decision parser started")
    for file in decision_files:
        medicine_struct = dec_parser.parse_file(file, directory, medicine_struct)
    log.info("Annex parser started")
    for file in annex_files:
        medicine_struct = annex_parser.parse_file(file, medicine_struct)
    log.info("EPAR parser started")
    for file in epar_files:
        medicine_struct = epar_parser.parse_file(file, directory, medicine_struct)
    log.info("OMAR parser started")
    for file in omar_files:
        medicine_struct = omar_parser.parse_file(file, medicine_struct)
    for file in odwar_files:
        medicine_struct.odwars.append({attr.pdf_file: file})
    return medicine_struct


def folder_has_no_pdf_json(directory: str, folder: str) -> bool:
    """
    Returns whether the given directory already has a pdf_parser.json file

    Args:
        directory (str): Main data directory
        folder (str): Medicine folder that might have a pdf_parser.json file

    Returns:
        bool: True if the given directory already has a pdf_parser.json file, False otherwise
    """
    for filename in listdir(path.join(directory, folder)):
        if "pdf_parser" in filename:
            return False
    return True


def datetime_serializer(date: datetime.datetime) -> str:
    """
    Datetime to string serializer for json dumping
    Convert datetime.datetime to string

    Args:
        date (datetime.datetime): date to convert to string

    """
    if isinstance(date, datetime.datetime):
        return date.__str__()
    if isinstance(date, datetime.date):
        return date.__str__()


if __name__ == "__main__":
    main('../../../data')
