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
        # webdata_json_list.append(get_webdata_json(path.join(directory, subdirectory)))

    print(medicine_json_list)

    all_json_results = open(path.join(directory, "all_json_results.json"), "w")
    json.dump(medicine_json_list, all_json_results)
    all_json_results.close()


def get_medicine_json(medicine_path: str, json_list: list):
    medicine_jsons = [file for file in listdir(medicine_path) if
                      path.isfile(path.join(medicine_path, file)) and "pdf_parser.json" in file]
    if len(medicine_jsons) <= 0:
        return

    with open(path.join(medicine_path, medicine_jsons[0])) as json_file:
        try:
            medicine_json_dir = json.load(json_file)
        except:
            return

    json_list.append(medicine_json_dir)


compile_json_files("D:\\Git_repos\\PharmaVisual\\medctrl-scraper\\PDF_scraper\\Text_scraper\\parsers\\test_data")
