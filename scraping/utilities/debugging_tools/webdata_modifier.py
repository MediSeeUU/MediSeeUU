import os.path as path
import json
import os
import datetime

import scraping.utilities.definitions.attributes as attr

active_withdrawn_path = "D:\Git_repos\MediSeeUU\data\\active_withdrawn"
medicine_folders = [path.join(active_withdrawn_path, folder) for folder in os.listdir(active_withdrawn_path) if "EU" in folder]
# print(medicine_folders)

for folder in medicine_folders:
    try:
        webdata_path = [path.join(folder, file) for file in os.listdir(folder) if "webdata" in file][0]
        filedates_path = [path.join(folder, file) for file in os.listdir(folder) if "filedates" in file][0]
    except Exception:
        continue

    try:
        with open(webdata_path) as webdata_file:
            webdata_dict = json.load(webdata_file)
    except Exception:
        continue

    try:
        with open(filedates_path) as filedates_file:
            filedates_dict = json.load(filedates_file)
    except Exception:
        continue

    webdata_dict[attr.filedates_web] = filedates_dict
    webdata_dict[attr.scrape_date_web] = str(datetime.datetime.today())

    with open(webdata_path, "w") as webdata_file:
        json.dump(webdata_dict, webdata_file, default=str)
    