import re
import pandas as pd
import logging
import scraping.file_parser.pdf_parser.parsed_info_struct as pis
import os
from os import path
import json
import scraping.file_parser.debugging_tools.json_compiler as json_compiler

test_location = "test_annex10_data"
log = logging.getLogger("file_parser.excel_parser")


def get_all(filename: str, excel_file: pd.DataFrame, data_dir: str) -> dict:
    """
    Gets all attributes of the annex 10 file and returns them in a dictionary

    Args:
        filename (str): name of the Excel file to be scraped
        excel_file (pd.DataFrame): the contents of the Excel file
        data_dir (str): Directory of the main data folder

    Returns:
        dict: Dictionary of all scraped attributes, named according to the bible
    """
    annex10 = {"filename": filename[:len(filename.split('.')[0])],  # removes extension
               "active_clock_elapseds": get_active_clock_elapsed(excel_file, data_dir)}
    return annex10


def parse_file(filename: str, directory: str, annex10s: list[dict], data_dir: str):
    """
    Gets all attributes from the annex 10 Excel file after parsing it

    Args:
        filename (str): name of the Excel file to be scraped
        directory (str): path of the directory containing the Excel file
        annex10s (list[dict]): list of currently scraped Excel file attributes
        data_dir (str): Directory of the main data folder


    Returns:
        list[dict]: all attributes contained in one dictionary per file, now updated
    """
    filepath = path.join(directory, filename)
    try:
        excel_data = pd.read_excel(filepath)
    except FileNotFoundError:  # TODO: Replace with pandas error
        log.warning("ANNEX 10 PARSER: File not found - " + filepath)
        return annex10s
    excel_data = clean_df(excel_data)
    res = get_all(filename, excel_data, data_dir)
    annex10s.append(res)
    return annex10s


def clean_df(excel_data: pd.DataFrame) -> pd.DataFrame:
    """
    Args:
        excel_data (pd.DataFrame): the contents of the Excel file

    Returns:
        pd.DataFrame: the cleaned contents of the Excel file
    """
    # Clean null lines
    excel_data = excel_data[~excel_data["Unnamed: 0"].isnull()]
    # Remove all before "Product Name"
    x = excel_data.index[excel_data["Unnamed: 0"] == "Product Name"].tolist()[0]
    excel_data = excel_data.truncate(before=x).reset_index()
    # Set index to first row
    excel_data.columns = excel_data.iloc[0]
    excel_data = excel_data.truncate(before=1).reset_index()
    # Remove redundant columns
    excel_data = excel_data.iloc[:, 2:]

    return excel_data


def get_active_clock_elapsed(excel_data: pd.DataFrame, data_dir: str) -> list[dict]:
    """
    Gets three attributes for each row in the dataframe: product name, active time elapsed, clock stop elapsed.
    Adds one item to the final list "res" containing a dictionary of these attributes

    Args:
        excel_data (pd.DataFrame): the contents of the Excel file
        data_dir (str): Directory of the main data folder

    Returns:
        list[dict]: list of dictionaries containing product name, active time elapsed, clock stop elapsed for each row.
    """
    res = []
    # Clean once more for nan values in active_time_elapsed
    excel_data = excel_data[~excel_data["Active Time Elapsed"].isnull()]

    # Get all relevant data from columns
    product_names = (excel_data["Product Name"].tolist())
    active_time_elapseds = (excel_data["Active Time Elapsed"].tolist())
    clock_stop_elapseds = (excel_data["Clock Stop Elapsed"].tolist())

    # Load all medicine data from all_json_results.json, created by json_compiler
    scraping_dir = data_dir.split('data')[0].strip('/') + "/scraping"
    all_json_results = open(path.join(scraping_dir, "all_json_results.json"), "r", encoding="utf-8")
    all_data = json.load(all_json_results)
    all_json_results.close()

    # Append info as dictionary
    for product_name, active_time_elapsed, clock_stop_elapsed in \
            zip(product_names, active_time_elapseds, clock_stop_elapseds):
        if product_name_in_epars(product_name.lower(), all_data):
            res.append({
                "product_name": product_name,
                "active_time_elapsed": active_time_elapsed,
                "clock_stop_elapsed": clock_stop_elapsed
            })
    return res


def product_name_in_epars(product_name: str, all_data: list[dict]) -> bool:
    """
    Check if EPAR exists for pdf_parser json containing a similar brand name to the product name

    Args:
        product_name (str): Product Name to check for in pdf_parser json
        all_data (list[dict]): All attributes from pdf_parser in one JSON file

    Returns:
        bool: True if product_name is found in one of the EPAR brand names
    """
    eu_num = ""
    for medicine in all_data:
        # Check if product_name in brand_name and get EU number
        if "eu_brand_name_current" in medicine.keys():
            if product_name in medicine["eu_brand_name_current"].lower() or \
                    medicine["eu_brand_name_current"].lower() in product_name:
                eu_num = medicine["eu_pnumber"]
    for medicine in all_data:
        # Check if found EU number has an EPAR
        if "eu_number" not in medicine.keys():
            continue
        if medicine["eu_number"] != eu_num.replace("/", "-"):
            continue
        if medicine["epars"]:
            return True
    return False


def run(data_folder_directory):
    # json_compiler.compile_json_files(data_folder_directory)

    annex10s = []
    for filename in os.listdir(test_location):
        annex10s = parse_file(filename, test_location, annex10s, data_folder_directory)

    f = open("annex10_parser.json", "w")
    f.write(str(annex10s))
    f.close()


run("../../../data")
