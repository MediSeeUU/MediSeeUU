from os import listdir
import os.path as path
import json


def compile_json_files(directory: str):
    subdirectories = [subdirectory for subdirectory in listdir(directory) if
                      path.isdir(path.join(directory, subdirectory))]

    medicine_json_list = []
    webdata_json_list = []

    for subdirectory in subdirectories:
        get_medicine_json(path.join(directory, subdirectory), medicine_json_list)

    # print(medicine_json_list)
    scraping_dir = directory.split('data')[0].strip('/') + "/scraping"
    all_json_results = open(path.join(scraping_dir, "all_json_results.json"), "w")
    json.dump(medicine_json_list, all_json_results)
    all_json_results.close()


def get_medicine_json(medicine_path: str, json_list: list):
    medicine_jsons = [file for file in listdir(medicine_path) if
                      path.isfile(path.join(medicine_path, file)) and ("webdata.json" in file or "pdf_parser.json" in file)]

    for medicine_json in medicine_jsons:
        with open(path.join(medicine_path, medicine_json)) as json_file:
            try:
                medicine_json_dir = json.load(json_file)
                json_list.append(medicine_json_dir)
            except:
                return

# Todo: Remove this when no longer needed
# compile_json_files("D:\\Git_repos\\PharmaVisual\\medctrl-scraper\\pdf_parser\\Text_scraper\\parsers\\test_data")
