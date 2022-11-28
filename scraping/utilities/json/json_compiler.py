from os import listdir
import os.path as path
import json


def compile_json_files(directory: str, save_dir: str, add_webdata: bool = True, add_pdfdata: bool = True):
    """
    Combines JSONs from PDF scraper and/or web scraper

    Args:
        directory (str): Data folder containing the categories of medicines:
        save_dir (str): Folder where all_json_results.json will be saved
        add_webdata (bool): Whether to add web data json files
        add_pdfdata (bool): Whether to add pdf data json files
    """
    meds_dir = f"{directory}/active_withdrawn"

    subdirectories = [subdirectory for subdirectory in listdir(meds_dir) if
                      path.isdir(path.join(meds_dir, subdirectory))]

    medicine_json_list = []

    for subdirectory in subdirectories:
        get_medicine_json(path.join(meds_dir, subdirectory), medicine_json_list, add_webdata, add_pdfdata)

    all_json_results = open(path.join(save_dir, "all_json_results.json"), "w")
    json.dump(medicine_json_list, all_json_results)
    all_json_results.close()


def get_medicine_json(medicine_path: str, json_list: list[dict], add_webdata: bool, add_pdfdata: bool):
    """

    Args:
        medicine_path (str): Path to medicine folder containing json files
        json_list (list[dict]): List of dictionaries from all json files
        add_webdata (bool): Whether to add web data json files
        add_pdfdata (bool): Whether to add pdf data json files
    """
    medicine_jsons = [file for file in listdir(medicine_path) if path.isfile(path.join(medicine_path, file))]
    if add_webdata and add_pdfdata:
        medicine_jsons = [file for file in medicine_jsons if "webdata.json" in file or "pdf_parser.json" in file]
    elif add_webdata:
        medicine_jsons = [file for file in medicine_jsons if "webdata.json" in file]
    elif add_pdfdata:
        medicine_jsons = [file for file in medicine_jsons if "pdf_parser.json" in file]

    for medicine_json in medicine_jsons:
        with open(path.join(medicine_path, medicine_json)) as json_file:
            try:
                medicine_json_dir = json.load(json_file)
                json_list.append(medicine_json_dir)
            # TODO: Add specific exception handling
            except:
                return
