import json
import logging
import os.path as path
from os import listdir

import scraping.combiner.attribute_combining_functions as acf
import scraping.utilities.definitions.attribute_objects as attr_obj
import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.sources as src

log = logging.getLogger("combiner")


def main(data_directory: str):
    """
    Combines all web data jsons and pdf_parser jsons into combined jsons

    Args:
        data_directory (str): Main data folder containing the active_withdrawn folder with medicines
    """
    log.info("Combining JSON files")
    active_withdrawn_folder = path.join(data_directory, "active_withdrawn")
    directory_folders = [folder for folder in listdir(active_withdrawn_folder) if
                         path.isdir(path.join(active_withdrawn_folder, folder)) and "EU" in folder]

    # Single-threaded parsing
    for folder in directory_folders:
        combine_folder(path.join(active_withdrawn_folder, folder), folder)

    log.info("Finished combining JSON files\n")


def create_file_dicts(filepath: str, folder_name: str) -> dict[str, any]:
    """
    Create dictionary of all sources with their attributes in a medicine folder

    Args:
        filepath (str): Path to the medicine folder
        folder_name (str): Name of the medicine folder

    Returns:
        dict[str, any]: Dictionary with sources as keys, and data of sources as attributes
    """
    file_dicts_keys = [src.decision, src.dec_initial, src.annex, src.anx_initial,
                       src.annex_10, src.epar, src.omar, src.web]
    file_dicts = dict.fromkeys(file_dicts_keys, {})

    # try to get main sources
    pdf_data = get_dict('pdf_parser', filepath, folder_name)
    file_dicts[src.web] = get_dict('webdata', filepath, folder_name)

    # get data from pdf_parser json
    decision_files = sorted(
        [(int(dictionary[attr.pdf_file][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["decisions"]],
        key=lambda x: x[0])
    annex_files = sorted(
        [(int(dictionary[attr.pdf_file][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["annexes"]],
        key=lambda x: x[0])

    # get current and initial files
    if len(decision_files) > 0:
        file_dicts[src.decision] = decision_files[-1][1]
        file_dicts[src.dec_initial] = decision_files[0][1]
    if len(annex_files) > 0:
        file_dicts[src.annex] = annex_files[-1][1]
        file_dicts[src.anx_initial] = annex_files[0][1]

    if len(pdf_data["epars"]) > 0:
        file_dicts[src.epar] = pdf_data["epars"][0]
    else:
        log.info(f"COMBINER: no epar found in pdf_data for {folder_name}")

    if len(pdf_data["omars"]) > 0:
        file_dicts[src.omar] = pdf_data["omars"][0]
    else:
        log.info(f"COMBINER: no omar found in pdf_data for {folder_name}")

    # fetch annex_10
    annex_10_path = path.join(filepath, "../../annex_10/annex_10_parser.json")
    if path.exists(annex_10_path):
        with open(annex_10_path, "r") as annex_10:
            file_dicts[src.annex_10] = json.load(annex_10)
    else:
        log.info(f"COMBINER: no annex_10 data found in {folder_name}")
    return file_dicts


def combine_folder(filepath: str, folder_name: str):
    """
    Combines the web data json and pdf_parser json into a combined.json for a medicine and saves this combined.json.

    Args:
        filepath (str): Path to the medicine folder
        folder_name (str): Name of the medicine folder
    """
    file_dicts = create_file_dicts(filepath, folder_name)
    combined_dict: dict[str, any] = {}

    for attribute in attr_obj.objects:
        value = attribute.combine_function(eu_pnumber=folder_name, attribute_name=attribute.name,
                                           sources=attribute.sources, file_dicts=file_dicts)
        date = acf.get_attribute_date(attribute.sources[0], file_dicts)
        combined_dict[attribute.name] = attribute.json_function(value=value, date=date)

    combined_json = open(path.join(filepath, folder_name + "_combined.json"), "w")
    json.dump(combined_dict, combined_json, default=str, indent=4)
    combined_json.close()


def get_dict(source: str, filepath: str, folder_name: str) -> dict[str, any]:
    """
    Gives the dictionary/data from the source "source" in folder/medicine "folder_name"

    Args:
        source (str): Name of the source
        filepath (str): Path to the medicine folder
        folder_name (str): Name of the medicine folder

    Returns:
        dict[str, any]: Dictionary of data in the given source
    """
    source_path = path.join(filepath, folder_name + f"_{source}.json")
    if not path.exists(source_path):
        log.warning(f"COMBINER: no {source}.json found in {filepath}")
        return {}
    with open(source_path, "r") as source_json:
        return json.load(source_json)
