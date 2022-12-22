from datetime import datetime
from os import listdir
import os.path as path
import json
import joblib
import multiprocessing
import scraping.combiner.attribute_combining_functions as acf
import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.attribute_objects as attr_obj
import scraping.utilities.definitions.sources as src
import logging

log = logging.getLogger("combiner")


# Main file to run all parsers
def main(data_directory: str):
    log.info("Combining JSON files")
    active_withdrawn_folder = path.join(data_directory, "active_withdrawn")
    directory_folders = [folder for folder in listdir(active_withdrawn_folder) if
                         path.isdir(path.join(active_withdrawn_folder, folder)) and "EU" in folder]
    #
    # # Use all the system's threads to maximize use of all hyper-threads
    # joblib.Parallel(n_jobs=max(int(multiprocessing.cpu_count() - 1), 1), require=None)(
    #     joblib.delayed(combine_folder)(path.join(active_withdrawn_folder, folder_name), folder_name) for folder_name in
    #     directory_folders)

    # Single-threaded parsing
    for folder in directory_folders:
        combine_folder(path.join(active_withdrawn_folder, folder), folder)

    log.info("Finished combining JSON files\n")


def create_file_dicts(filepath: str, folder_name: str) -> dict[str, any]:
    file_dicts_keys = [src.decision, src.decision_initial, src.annex, src.annex_initial,
                       src.annex_10, src.epar, src.omar, src.web]
    file_dicts = dict.fromkeys(file_dicts_keys, {})

    # try to get sources
    # TODO: dit zou gelijk samen kunnen met attr. enzo
    pdf_data = get_dict('pdf_parser', filepath, folder_name)
    file_dicts[src.web] = get_dict('webdata', filepath, folder_name)

    decision_files = sorted(
        [(int(dictionary[attr.pdf_file][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["decisions"]],
        key=lambda x: x[0])
    annex_files = sorted(
        [(int(dictionary[attr.pdf_file][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["annexes"]],
        key=lambda x: x[0])

    # TODO: functie met len
    if len(decision_files) > 0:
        file_dicts[src.decision] = decision_files[-1][1]
        file_dicts[src.decision_initial] = decision_files[0][1]
    if len(annex_files) > 0:
        file_dicts[src.annex] = annex_files[-1][1]
        file_dicts[src.annex_initial] = annex_files[0][1]

    try:
        file_dicts[src.epar] = pdf_data["epars"][0]
    except IndexError:
        log.info(f"COMBINER: no epar found in pdf_data for {folder_name}")

    try:
        file_dicts[src.omar] = pdf_data["omars"][0]
    except IndexError:
        log.info(f"COMBINER: no omar found in pdf_data for {folder_name}")

    try:
        annex_10_path = path.join(filepath, "../../annex_10")
        with open(path.join(annex_10_path, "annex_10_parser.json"), "r") as annex_10:
            file_dicts[src.annex_10] = json.load(annex_10)
    except FileNotFoundError:
        log.info(f"COMBINER: no omar found in pdf_data for {folder_name}")

    return file_dicts


def combine_folder(filepath: str, folder_name: str):
    """

    Args:
        filepath:
        folder_name:

    Returns:

    """
    file_dicts = create_file_dicts(filepath, folder_name)
    combined_dict: dict[str, any] = {}

    # TODO: hier een functie van
    for attribute in attr_obj.all_attribute_objects:
        try:
            value = attribute.combine_function(folder_name, attribute.name, attribute.sources, file_dicts)
            date = acf.get_attribute_date(attribute.sources[0], file_dicts)
            combined_dict[attribute.name] = attribute.json_function(value, date)
        except Exception:
            log.warning("COMBINER: failed to get", attribute.name, "in", folder_name)

    combined_json = open(path.join(filepath, folder_name + "_combined.json"), "w")
    json.dump(combined_dict, combined_json, default=str)
    combined_json.close()


# TODO: misschien andere except dan filenotfounderror?
def get_dict(source: str, filepath: str, folder_name: str) -> dict:
    """

    Args:
        source:
        filepath:
        folder_name:

    Returns:

    """
    try:
        with open(path.join(filepath, folder_name + f"_{source}.json"), "r") as source_json:
            return json.load(source_json)
    except FileNotFoundError:
        log.warning(f"COMBINER: no {source}.json found in {filepath}")
        return {}
    except Exception:
        log.error("other error")


def sources_to_dicts(sources: list[str], file_dicts: dict[str, dict]) -> list[dict]:
    """

    Args:
        sources:
        file_dicts:

    Returns:

    """
    source_dicts: list[str] = []

    for source in sources:
        source_dicts.append(file_dicts[source])

    return source_dicts


# datetime to string serializer for json dumping
def date_serializer(date: datetime.date) -> str:
    """

    Args:
        date:

    Returns:

    """
    if isinstance(date, datetime.date):
        return date.__str__()


def datetime_converter(datetime: str) -> str:
    """_summary_

    Args:
        datetime (str): _description_

    Returns:
        str: _description_
    """
    return datetime.split('+').split(" ")[0]

# if __name__ == "__main__":
#     main('..\..\..\data')


# combine_folder("..\\..\\data\\active_withdrawn\\EU-1-00-130", "EU-1-00-130")
# print(type(attr_obj.all_attributes))
# print(attr_obj.all_attributes)
