from datetime import datetime
from os import listdir
import os.path as path
import json
import joblib
import multiprocessing

class filetype(Enum):
    decision = "decision"
    annex = "annex"
    epar = "epar"
    omar = "omar"
    ec_site = "ec_site"
    ema_site = "ema_site"
    excel = "excel"


# Main file to run all parsers
def main(directory: str):
    return

    print("Combining JSON files")
    directory_folders = [folder for folder in listdir(directory) if path.isdir(path.join(directory, folder))]

    # Use all the system's threads to maximize use of all hyper-threads
    joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
        joblib.delayed(combine_folder)(path.join(directory, folder_name), folder_name) for folder_name in
        directory_folders)
    print("Finished combining JSON files\n")

    # Single-threaded parsing
    # for folder in directory_folders:
    #     parse_folder(path.join(directory, folder), folder)


# scraping on medicine folder level
def combine_folder(directory: str, folder_name):
    try:
        pdf_json = json.load(folder_name + "_pdf_parser.json")
    except Exception as exception:
        print(str(exception))
        print(f"skipped combining: {folder_name}")
        return

    try:    
        web_json = json.load(folder_name + "_web_parser.json")
    except Exception as exception:
        print(str(exception))
        print(f"skipped combining: {folder_name}")
        return

    #attribute values
    attribute_values: dict[str, (str, str, datetime.date)]

    # list of attributeCombiningFunctions with priorities
    
    # loop through list and update the output json
    



    # dump json result to medicine folder directory
    json_file = open(path.join(directory, folder_name) + "_combined.json", "w")
    combined_attributes_json = json.dumps(attribute_values, date_serializer)
    json_file.write(combined_attributes_json)
    json_file.close()


# datetime to string serializer for json dumping
def date_serializer(date: datetime.date):
    if isinstance(date, datetime.date):
        return date.__str__()

if __name__ == "__main__":
    main('..\..\..\data')
