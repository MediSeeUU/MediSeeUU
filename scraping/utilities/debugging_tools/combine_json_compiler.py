import json
import os.path as path
from os import listdir


def compile_json_files(directory: str):
    """
    Combines JSONs from PDF scraper and/or web scraper

    Args:
        directory (str): Data folder containing medicines:
        add_webdata (bool): Whether to add web data json files
        add_pdfdata (bool): Whether to add pdf data json files
    """
    subdirectories = [subdirectory for subdirectory in listdir(directory) if
                      path.isdir(path.join(directory, subdirectory))]

    medicine_json_list = []

    for subdirectory in subdirectories:
        get_combine_json(path.join(directory, subdirectory), medicine_json_list)

    # print(medicine_json_list)
    scraping_dir = directory.split('data')[0].strip('/') + "/scraping"
    all_json_results = open(path.join(scraping_dir, "all_combined_results.json"), "w")
    json.dump(medicine_json_list, all_json_results)
    all_json_results.close()

    eu_numbers = open(path.join(directory, "eu_numbers.json"), "w")
    json.dump(subdirectories, eu_numbers)
    eu_numbers.close()


def get_combine_json(medicine_path: str, json_list: list[dict]):
    """

    Args:
        medicine_path (str): Path to medicine folder containing json files
        json_list (list[dict]): List of dictionaries from all json files
        add_webdata (bool): Whether to add web data json files
        add_pdfdata (bool): Whether to add pdf data json files
    """
    medicine_jsons = [file for file in listdir(medicine_path) if path.isfile(path.join(medicine_path, file)) and "combined" in file]

    for medicine_json in medicine_jsons:
        with open(path.join(medicine_path, medicine_json)) as json_file:
            try:
                medicine_json_dir = json.load(json_file)
                json_list.append(medicine_json_dir)
            # TODO: Add specific exception handling
            except:
                print("exception")
                return

# Todo: Remove this when no longer needed
compile_json_files("D:\\Git_repos\\mediSeeUU\\data")
