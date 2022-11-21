from datetime import datetime
from os import listdir
import os.path as path
import json
import joblib
import multiprocessing
import scraping.definitions.value as value
import scraping.definitions.attributes as attr


# Main file to run all parsers
def main(directory: str):
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


def combine_folder(filepath: str, folder_name: str):
    """

    Args:
        filepath:
        folder_name:

    Returns:

    """
    file_dicts_keys = [attr.decision, attr.decision_initial, attr.annex, attr.annex_initial,
                    attr.epar, attr.omar, attr.web, attr.file_dates]
    file_dicts = dict.fromkeys(file_dicts_keys,{})
    combined_dict: dict[str, any] = {}

    # try to get sources
    # TODO: dit zou gelijk samen kunnen met attr. enzo
    pdf_data = get_dict('pdf_parser', filepath, folder_name)
    file_dicts[attr.file_dates] = get_dict('filedates', filepath, folder_name)
    file_dicts[attr.web] = get_dict('webdata', filepath, folder_name)

    decision_files = sorted(
        [(int(dictionary["filename"][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["decisions"]],
        key=lambda x: x[0])
    annex_files = sorted(
        [(int(dictionary["pdf_file"][:-4].split("_")[-1]), dictionary) for dictionary in pdf_data["annexes"]],
        key=lambda x: x[0])


    # TODO: functie met len
    if len(decision_files) > 0:
        file_dicts[attr.decision] = decision_files[-1][1]
        file_dicts[attr.decision_initial] = decision_files[0][1]
    if len(annex_files) > 0:
        file_dicts[attr.annex] = annex_files[-1][1]
        file_dicts[attr.annex_initial] = annex_files[0][1]

    try:
        file_dicts[attr.epar] = pdf_data["epars"][0]
    except IndexError:
        print(f"COMBINER: no epar found in pdf_data for {folder_name}")

    try:
        file_dicts[attr.omar] = pdf_data["omars"][0]
    except IndexError:
        print(f"COMBINER: no omar found in pdf_data for {folder_name}")

    # TODO: hier een functie van
    for attribute in attr.all_attributes:
        value, all_equal = get_attribute(attribute.name, sources_to_dicts(attribute.sources, file_dicts),
                                         attribute.combine)
        combined_dict[attribute.name] = value

        # if not all_equal:
            # print("found multiple values for " + attribute.name + ": " + value + " in " + str(
            #     sources_to_dicts(attribute.sources, file_dicts)))

    combined_json = open(path.join(filepath, folder_name + "_combined.json"), "w")
    json.dump(combined_dict, combined_json)
    combined_json.close()

# TODO: misschien andere except dan filenotfounderror?
def get_dict(source: str, filepath: str, folder_name: str) -> dict :
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
        print(f"COMBINER: no {source}.json found in " + filepath)
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


def get_attribute(attribute_name: str, dicts: list[dict], combine_attributes=False) -> tuple[str, bool]:
    """

    Args:
        attribute_name:
        dicts:
        combine_attributes:

    Returns:

    """
    attributes: set[str] = []
    # print(attribute_name + ": " + str(dicts))
    for dict in dicts:
        try:
            attributes.append(dict[attribute_name])
        except Exception:
            print()
            # print(attribute_name + ": " + str(dicts))
            # print(attribute_name + " not found")

    all_equal = len(set(attributes)) == 1

    if combine_attributes:
        return (" / ".join(attributes), all_equal)

    attributes.append(value.not_found)
    return (attributes[0], all_equal)


# datetime to string serializer for json dumping
def date_serializer(date: datetime.date) -> str:
    """

    Args:
        date:

    Returns:

    """
    if isinstance(date, datetime.date):
        return date.__str__()


# if __name__ == "__main__":
#     main('..\..\..\data')


combine_folder("..\\..\\data\\EU-1-99-126", "EU-1-99-126")
print(type(attr.all_attributes))
print(attr.all_attributes)

