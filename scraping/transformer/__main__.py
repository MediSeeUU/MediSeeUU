import logging
from os import listdir, path
import json
import scraping.utilities.definitions.attribute_objects as attr_objects
import scraping.utilities.definitions.attribute_values as values

log = logging.getLogger("transformer")

all_humans = [obj.name for obj in list(attr_objects.all_attribute_objects) if not obj.is_orphan]
all_orphans = [obj.name for obj in list(attr_objects.all_attribute_objects) if obj.is_orphan]


def convert_json(combined_json_path: str):
    """
    Converts one JSON to the right format for the database
    Args:
        combined_json_path (str): Path to the JSON file
    """
    with open(combined_json_path) as combined_json:
        json_data = json.load(combined_json)
    final_json = {}
    if json_data["orphan_status"] == 'h':
        get_final_json(final_json, json_data, all_humans)
    elif json_data["orphan_status"] == 'o':
        get_final_json(final_json, json_data, all_orphans)

    save_transformed_json(combined_json_path, final_json)


def save_transformed_json(combined_json_path: str, final_json: dict):
    """
    Saves transformed JSON for that medicine
    Args:
        combined_json_path (str): Location of the combined JSON
        final_json (dict): Dictionary of all human or orphan attributes
    """
    transformed_json_path = f"{combined_json_path.split('combined.json')[0]}transformed.json"
    with open(transformed_json_path, 'w') as transformed_file:
        json.dump(final_json, transformed_file, indent=4)


def get_final_json(final_json: dict, json_data: dict, all_names: list):
    """
    Returns JSON filtered by only human or orphan attributes
    Args:
        final_json (dict): Dictionary of all human or orphan attributes
        json_data (dict): Dictionary of all attributes: combined.json
        all_names (list): Names of all attributes of the human or orphan medicine to be filtered on
    """
    not_found_str = "Not found"
    for name, value in json_data.items():
        if name not in all_names:
            continue
        if values.not_found == value or values.combiner_not_found == value:
            value = not_found_str
        if "url" not in name:
            final_json[name] = value
        elif value[0]["value"] == values.not_found or value[0]["value"] == values.combiner_not_found:
            value[0]["value"] = not_found_str

        final_json[name] = value


# Main file to run all parsers
def main(directory: str):
    """
    Given a folder containing medicine folders, converts each combined_attributes.json
    to the right format for the database.

    Args:
        directory: data folder, containing medicine folders
    """
    log.info(f"=== Transforming all combined_attributes.json files ===")

    # Get all combined.json files, and convert them to the right format
    for folder in listdir(f"{directory}/active_withdrawn"):
        med_path = f"{directory}/active_withdrawn/{folder}"
        combined_file = [file for file in listdir(med_path) if path.isfile(path.join(med_path, file))
                         and "combined.json" in file][0]
        combined_json_path = f"{med_path}/{combined_file}"
        convert_json(combined_json_path)

    log.info(f"=== Done transforming ===")


if __name__ == "__main__":
    main('../../../data')
