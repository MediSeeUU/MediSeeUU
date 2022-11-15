import re
import pandas as pd
import logging
import scraping.file_parser.pdf_parser.parsed_info_struct as pis
import os
from os import path

test_location = "test_annex10_data"
log = logging.getLogger("file_parser.excel_parser")


def get_all(filename: str, excel_file: pd.DataFrame) -> dict:
    """
    Gets all attributes of the annex 10 file and returns them in a dictionary

    Args:
        filename (str): name of the Excel file to be scraped
        excel_file (pd.DataFrame): the contents of the Excel file

    Returns:
        dict: Dictionary of all scraped attributes, named according to the bible
    """
    annex10 = {"filename": filename[:len(filename.split('.')[0])]}  # removes extension
               # "ema_procedure_start_initial": get_date(excel_file)}
    return annex10


def parse_file(filename: str, directory: str, annex10s: list[dict]):
    """
    Gets all attributes from the annex 10 Excel file after parsing it

    Args:
        filename (str): name of the Excel file to be scraped
        directory (str): path of the directory containing the Excel file
        annex10s (list[dict]): list of currently scraped Excel file attributes

    Returns:
        list[dict]: all attributes contained in one dictionary per file, now updated
    """
    filepath = path.join(directory, filename)
    try:
        excel_data = pd.read_excel(filepath)
    except FileNotFoundError:  # TODO: Replace with pandas error
        log.warning("ANNEX 10 PARSER: File not found - " + filepath)
        return annex10s
    res = get_all(filename, excel_data)
    annex10s.append(res)
    return annex10s


for filename in os.listdir(test_location):
    annex10s = []
    print(parse_file(filename, test_location, annex10s))
