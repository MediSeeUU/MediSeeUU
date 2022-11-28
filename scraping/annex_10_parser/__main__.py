import pandas as pd
import os
from os import path
import json
from datetime import datetime
import logging
import scraping.utilities.json.json_compiler as json_compiler

log = logging.getLogger("file_parser.annex_10_parser")
annex_10_json_file = "annex_10_parser.json"


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


def parse_file(filename: str, directory: str, annex10s: list[dict], data_dir: str) -> list[dict]:
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
    if ".xlsx" not in filepath:
        return annex10s
    try:
        excel_data = pd.read_excel(filepath)
    except FileNotFoundError:
        log.warning("ANNEX 10 PARSER: File not found - " + filepath)
        return annex10s
    excel_data = clean_df(excel_data)
    res = get_all(filename, excel_data, data_dir)
    annex10s.append(res)
    return annex10s


def clean_df(excel_data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the Excel file by removing null lines, starting rows from first Product Name value,
    naming the columns, and removing other columns than the last two

    Args:
        excel_data (pd.DataFrame): the contents of the Excel file

    Returns:
        pd.DataFrame: the cleaned contents of the Excel file
    """
    # Clean null lines
    excel_data = excel_data[~excel_data["Unnamed: 0"].isnull()]
    # Remove all rows before "Product Name"
    x = excel_data.index[excel_data["Unnamed: 0"] == "Product Name"].tolist()[0]
    excel_data = excel_data.truncate(before=x).reset_index()
    # Set column names
    excel_data.columns = excel_data.iloc[0]
    excel_data = excel_data.truncate(before=1).reset_index()
    # Remove redundant columns, only the last two columns contain the clock times we need.
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
    opinion_dates = (excel_data["Opinion Date"].tolist())
    active_time_elapseds = (excel_data["Active Time Elapsed"].tolist())
    clock_stop_elapseds = (excel_data["Clock Stop Elapsed"].tolist())

    # Load all medicine data from all_json_results.json, created by json_compiler
    all_json_results = open(path.join(f"{data_dir}/annex_10", "all_json_results.json"), "r", encoding="utf-8")
    all_data = json.load(all_json_results)
    all_json_results.close()

    # Append info as dictionary
    for product_name, opinion_date, active_time_elapsed, clock_stop_elapsed in \
            zip(product_names, opinion_dates, active_time_elapseds, clock_stop_elapseds):
        product_name_found, eu_num = product_name_in_epars(product_name.lower(), all_data, opinion_date)
        if product_name_found:
            res.append({
                "eu_number": eu_num,
                "active_time_elapsed": active_time_elapsed,
                "clock_stop_elapsed": clock_stop_elapsed
            })
    return res


def product_name_in_epars(product_name: str, all_data: list[dict], opinion_date: str) -> tuple[bool, str]:
    """
    Check if EPAR exists for pdf_parser json containing a similar brand name to the product name

    Args:
        product_name (str): Product Name to check for in pdf_parser json
        all_data (list[dict]): All attributes from pdf_parser in one JSON file
        opinion_date (str): Opinion date of the product, to be checked with chml_opinion_date in EPAR file

    Returns:
        (tuple[bool, str]): (True, EU_num) if product_name is found in one of the EPAR brand names, otherwise (False, "")
    """
    eu_num = ""
    if type(opinion_date) == datetime:
        opinion_date = opinion_date.strftime("%d/%m/%Y")
    opinion_date = datetime.strptime(opinion_date, '%d/%m/%Y')

    for medicine in all_data:
        # Check if product_name in brand_name and get EU number
        if "eu_brand_name_current" in medicine.keys():
            if product_name in medicine["eu_brand_name_current"].lower() or \
                    medicine["eu_brand_name_current"].lower() in product_name:
                eu_num = medicine["eu_pnumber"].replace("/", "-")
    for medicine in all_data:
        # Check if found EU number has an EPAR
        if "eu_number" not in medicine.keys():
            continue
        if medicine["eu_number"] != eu_num:
            continue
        if not medicine["epars"]:
            continue
        chmp_opinion_date = medicine["epars"][0]["chmp_opinion_date"]
        if chmp_opinion_date == "no_chmp_found":
            log.warning(f"Annex_10_parser: no chmp opinion date found in EPAR for {eu_num}")
            continue
        chmp_opinion_date = datetime.strptime(chmp_opinion_date, '%d/%m/%Y')
        # Check if the chmp_opinion_date and opinion_date are within 4 days of each other
        if abs((chmp_opinion_date - opinion_date).days) < 4:
            return True, eu_num
        # Print EU number, Product name, optinion date from EPAR, and opinion date from Excel file
        # print(eu_num + " - " + product_name + " - " + str(chmp_opinion_date).split(" ")[0] + " - " + str(opinion_date).split(" ")[0])
    return False, ""


def annexes_already_parsed(annex_10_folder: str) -> bool:
    """
    Return True if file already exists and last annex is included

    Args:
        annex_10_folder (str): folder containing annex 10 Excel files

    Returns:
        bool: True if file already exists and last annex is included, False otherwise
    """
    all_annexes_parsed = False
    if os.path.exists(annex_10_json_file):
        try:
            f = open(annex_10_json_file, "r", encoding="utf-8")
            parsed_data = json.load(f)
            for filename in os.listdir(annex_10_folder):
                if filename.split(".")[0] in parsed_data:
                    all_annexes_parsed = True
        except FileNotFoundError:
            log.error(f"{annex_10_json_file} not found.")
        except json.decoder.JSONDecodeError as error:
            log.error(f"Can't open {annex_10_json_file}: Decode error | " + str(error))
        if all_annexes_parsed:
            log.info("All annexes in folder were already parsed")
            return True
    return False


def main(data_folder_directory: str, annex_folder_name: str = "json"):
    """
    Scrape all annex 10 files

    Args:
        data_folder_directory (str): Data folder, containing medicine folders
        annex_folder_name (str): Name of the folder containing the annex 10 files
    """
    annex_10_folder = path.join(data_folder_directory, annex_folder_name)

    if not os.path.exists(annex_10_folder):
        log.error(f"Annex 10 folder {annex_10_folder} does not exist")
        return

    # Skip if file already exists and last annex is included
    if annexes_already_parsed(annex_10_folder):
        return

    json_compiler.compile_json_files(data_folder_directory, annex_10_folder, add_webdata=True, add_pdfdata=True)
    annex_10_folder = path.join(data_folder_directory, annex_folder_name)

    annex10s = []
    for filename in os.listdir(annex_10_folder):
        annex10s = parse_file(filename, annex_10_folder, annex10s, data_folder_directory)

    f = open(path.join(annex_10_folder, annex_10_json_file), "w")
    json_to_write = json.dumps(annex10s)
    f.write(json_to_write)
    f.close()


if __name__ == "__main__":
    main("../../../data")
