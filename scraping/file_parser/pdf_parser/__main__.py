import scraping.file_parser.pdf_parser.parsed_info_struct as pis
from os import listdir
import os.path as path
import json
import scraping.logger as logger
import joblib
from datetime import datetime
import multiprocessing

# for main
from scraping.file_parser.pdf_parser.parsers import dec_parser
from scraping.file_parser.pdf_parser.parsers import epar_parser
from scraping.file_parser.pdf_parser.parsers import omar_parser
from scraping.file_parser.pdf_parser.parsers import annex_parser


# Main file to run all parsers
def main(directory: str):
    """
    given a folder containing medicine folders, parses each folder in parallel

    Args:
        directory: data folder, containing medicine folders
    """
    log = logger.PDFLogger.log
    log.info(f"=== NEW LOG {datetime.today()} ===")
    directory_folders = [folder for folder in listdir(directory) if path.isdir(path.join(directory, folder))]

    # Use all the system's threads to maximize use of all hyper-threads
    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(parse_folder)(path.join(directory, folder_name), folder_name) for folder_name in
        directory_folders)
    log.info("Done parsing PDF files!")

    # Single-threaded parsing
    # for folder in directory_folders:
    #     parse_folder(path.join(directory, folder), folder)


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
    # Annex 10 folder should be skipped
    if "annex" in directory:
        return

    # struct that contains all scraped attributes dicts as well as eu_number and date of parsing
    medicine_struct = pis.ParsedInfoStruct(folder_name)

    # update list of files and filter out relevant files for each parser
    annex_files, decision_files, epar_files, omar_files = get_files(directory)

    # call scrapers on correct files and update medicine struct
    medicine_struct = run_scrapers(directory, annex_files, decision_files, epar_files, omar_files, medicine_struct)

    # dump json result to medicine folder directory
    json_file = open(path.join(directory, folder_name) + "_pdf_parser.json", "w")
    medicine_struct_json = json.dumps(pis.asdict(medicine_struct), default=datetime_serializer)
    json_file.write(medicine_struct_json)
    json_file.close()


def get_files(directory: str) -> (list[str], list[str], list[str], list[str]):
    """
    Get all PDF and XML files per PDF type

    Args:
        directory (str): Location of the medicine containing PDF files

    Returns:
        (list[str], list[str], list[str], list[str]): List of PDF file names for each of the 4 PDF types
    """
    directory_files = [file for file in listdir(directory) if path.isfile(path.join(directory, file))]
    decision_files = [file for file in directory_files if "dec" in file and ".xml" not in file]
    annex_files = [path.join(directory, file) for file in directory_files if "anx" in file and ".xml" in file]
    epar_files = [file for file in directory_files if
                  ("public-assessment-report" in file or "procedural-steps-taken" in file) and ".xml" in file]
    omar_files = [path.join(directory, file) for file in directory_files if
                  ("omar" in file or "orphan" in file) and ".xml" in file]
    return annex_files, decision_files, epar_files, omar_files


def run_scrapers(directory: str, annex_files: list[str], decision_files: list[str], epar_files: list[str],
                 omar_files: list[str], medicine_struct: pis.ParsedInfoStruct):
    """
    Scraping all XML or PDF files and updating medicine_struct with the scraped attributes

    Args:
        directory (list[str]): directory of folder containing the files
        annex_files (list[str]): list of file names for annex files
        decision_files (list[str]): list of file names for decisions files
        epar_files (list[str]): list of file names for epar files
        omar_files (list[str]): list of file names for omar files
        medicine_struct (pis.ParsedInfoStruct): struct to add parsed attributes to

    Returns:
        pis.ParsedInfoStruct: Medicine structure containing scraped attributes
    """
    for file in decision_files:
        medicine_struct = dec_parser.parse_file(file, directory, medicine_struct)
    for file in annex_files:
        medicine_struct = annex_parser.parse_file(file, medicine_struct)
    for file in epar_files:
        medicine_struct = epar_parser.parse_file(file, directory, medicine_struct)
    for file in omar_files:
        medicine_struct = omar_parser.parse_file(file, medicine_struct)
    return medicine_struct


def datetime_serializer(date: pis.datetime.datetime):
    """
    Datetime to string serializer for json dumping
    Convert datetime.datetime to string

    Args:
        date (pis.datetime.datetime): date to convert to string

    """
    if isinstance(date, pis.datetime.datetime):
        return date.__str__()


if __name__ == "__main__":
    main('../../../data')