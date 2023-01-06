from datetime import datetime
from os import listdir
import os.path as path
import json
import scraping.combiner.attribute_combining_functions as acf
import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.attribute_objects as attr_obj
import scraping.utilities.definitions.sources as src
import logging

log = logging.getLogger("combiner")
# log.disabled = True


# Main file to run all parsers
def main(data_directory: str):
    log.info("Combining JSON files")
    active_withdrawn_folder = path.join(data_directory, "active_withdrawn")
    directory_folders = [folder for folder in listdir(active_withdrawn_folder) if
                         path.isdir(path.join(active_withdrawn_folder, folder)) and "EU" in folder]

    # Single-threaded parsing
    for folder in directory_folders:
        combine_folder(path.join(active_withdrawn_folder, folder), folder)

    log.info("Finished combining JSON files\n")


def create_file_dicts(filepath: str, folder_name: str) -> dict[str, any]:
    file_dicts_keys = [src.decision, src.dec_initial, src.annex, src.anx_initial,
                       src.annex_10, src.epar, src.omar, src.web]
    file_dicts = dict.fromkeys(file_dicts_keys, {})

    # try to get sources
    # TODO: dit zou gelijk samen kunnen met attr. enzo
    pdf_data = get_dict('pdf_parser', filepath, folder_name)
    file_dicts[src.web] = get_dict('webdata', filepath, folder_name)

    # get respective parts from pdf_parser json
    decision_files = sorted(
        [(int(dictionary[attr.pdf_file][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["decisions"]],
        key=lambda x: x[0])
    annex_files = sorted(
        [(int(dictionary[attr.pdf_file][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["annexes"]],
        key=lambda x: x[0])

    # get current en initial files
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
    try:
        annex_10_path = path.join(filepath, "../../annex_10")
        with open(path.join(annex_10_path, "annex_10_parser.json"), "r") as annex_10:
            file_dicts[src.annex_10] = json.load(annex_10)
    except FileNotFoundError:
        log.info(f"COMBINER: no annex_10 data found in {folder_name}")

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
    for attribute in attr_obj.objects:
        try:
            value = attribute.combine_function(eu_pnumber=folder_name, attribute_name=attribute.name,
                                               sources=attribute.sources, file_dicts=file_dicts)
            date = acf.get_attribute_date(attribute.sources[0], file_dicts)
            combined_dict[attribute.name] = attribute.json_function(value, date)
        except Exception:
            log.info(f"COMBINER: failed to get {attribute.name} in {folder_name}")

    combined_json = open(path.join(filepath, folder_name + "_combined.json"), "w")
    json.dump(combined_dict, combined_json, default=str, indent=4)
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
    if source == "pdf_data":
        return {
            "eu_number": None,
            "parse_date": None,
            "annexes": [],
            "decisions": [],
            "epars": [],
            "omars": [],
            "odwars": []
        }

    try:
        with open(path.join(filepath, folder_name + f"_{source}.json"), "r") as source_json:
            return json.load(source_json)
    except FileNotFoundError:
        log.warning(f"COMBINER: no {source}.json found in {filepath}")
    except Exception as e:
        log.error(f"COMBINER: {e} for {source}.json in {filepath}")

    return {}


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
