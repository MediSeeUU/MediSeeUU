import json
import logging
from os import listdir, path

import scraping.utilities.definitions.attribute_objects as attr_objects
import scraping.utilities.definitions.attribute_values as values
import scraping.utilities.definitions.attributes as attr

log = logging.getLogger("transformer")

all_humans = [obj.name for obj in list(attr_objects.objects) if not obj.is_orphan]
all_orphans = [obj.name for obj in list(attr_objects.objects) if obj.is_orphan or
               obj.name == attr.orphan_status]
omar_conditions = []

skip_attr = [
    attr.eu_orphan_con_current
]
eu_orphan_con_currents = {}


def convert_json(combined_json_path: str):
    """
    Converts one JSON to the right format for the database
    Args:
        combined_json_path (str): Path to the JSON file
    """
    global omar_conditions

    with open(combined_json_path) as combined_json:
        json_data = json.load(combined_json)
    final_json = {}
    if json_data["orphan_status"] == 'h':
        get_final_json(final_json, json_data, all_humans)
    elif json_data["orphan_status"] == 'o':
        get_final_json(final_json, json_data, all_orphans)

    if "ema_omar_condition" in json_data.keys():
        if isinstance(json_data["ema_omar_condition"], list):
            omar_conditions += json_data["ema_omar_condition"]
            json_data.pop("ema_omar_condition")

    if attr.eu_orphan_con_current in json_data.keys():
        eu_orphan_con_current = json_data[attr.eu_orphan_con_current]
        if isinstance(eu_orphan_con_current, list):
            transform_orphan_cons(eu_orphan_con_current)
            json_data.pop(attr.eu_orphan_con_current)

    transformed_json_path = f"{combined_json_path.split('combined.json')[0]}transformed.json"
    save_transformed_json(transformed_json_path, final_json)


def transform_orphan_cons(eu_orphan_con_current: list):
    """
    Transforms eu_orphan_con_current objects and inserts it into the global eu_orphan_con_currents dict

    Args:
        eu_orphan_con_current (list): List of eu_orphan_con_current objects
    """
    global eu_orphan_con_currents

    for orphan_con_object in eu_orphan_con_current:
        scrape_date = orphan_con_object["date"]

        value = orphan_con_object["value"]
        if not isinstance(value, list):
            continue

        for orphan_con_value in value:
            value_dict = {}
            eu_num = orphan_con_value["eu_num"]
            value_dict["indication"] = orphan_con_value["indication"]
            value_dict["link_date"] = orphan_con_value["link_date"]

            # This check is only done because end date is not implemented yet
            value_dict["end_date"] = "Not found"
            if "end_date" in orphan_con_value:
                value_dict["end_date"] = orphan_con_value["end_date"]

            full_dict = {
                "value": value_dict,
                "date": scrape_date
            }

            if eu_num in eu_orphan_con_currents:
                eu_orphan_con_currents[eu_num].append(full_dict)
            else:
                eu_orphan_con_currents[eu_num] = [full_dict]


def save_transformed_json(transformed_json_path: str, final_json: dict):
    """
    Saves transformed JSON for that medicine
    Args:
        transformed_json_path (str): Location of the transformed JSON
        final_json (dict): Dictionary of all human or orphan attributes
    """
    with open(transformed_json_path, 'w') as transformed_file:
        json.dump(final_json, transformed_file, indent=4)


def get_final_json(final_json: dict, json_data: dict, all_names: list):
    """
    Returns JSON filtered by only human or orphan attributes
    Also replaces all not_found variants by "Not found"
    Args:
        final_json (dict): Dictionary of all human or orphan attributes
        json_data (dict): Dictionary of all attributes: combined.json
        all_names (list): Names of all attributes of the human or orphan medicine to be filtered on
    """
    not_found_str = "Not found"
    for name, value in json_data.items():
        if name not in all_names:
            continue
        if name in skip_attr:
            continue
        if values.not_found == value or values.url_not_found == value:
            value = not_found_str
        if name == "eu_od_pnumber" and value == not_found_str:
            continue
        if isinstance(value, dict):
            replace_not_found_dict(not_found_str, value)
        elif not isinstance(value, list) or len(value) < 1:
            final_json[name] = value
            continue
        for sub_key, sub_value in enumerate(value):
            replace_not_found_list_dict(not_found_str, sub_key, sub_value, value)
        final_json[name] = value


def replace_not_found_list_dict(not_found_str: str, sub_key: int, sub_value: dict | str, value: dict):
    """
    Replaces not_found_scraper with not_found_string for a sub_value in a list of dictionaries
    Args:
        not_found_str (str): "Not found"
        sub_key (int): Key of dictionary in list
        sub_value (dict | str): Value of dictionary in list
        value (dict): list of dictionaries in combined.json
    """
    if not isinstance(sub_value, dict):
        if sub_value == values.not_found or sub_value == values.url_not_found:
            value[sub_key] = not_found_str
    elif "value" not in sub_value.keys():
        for k, v in sub_value.items():
            if v != values.not_found and v != values.url_not_found:
                continue
            value[sub_key][k] = not_found_str
    elif sub_value["value"] == values.not_found or sub_value["value"] == values.url_not_found:
        value[sub_key]["value"] = not_found_str


def replace_not_found_dict(not_found_str: str, value: dict):
    """
    Replaces not_found_scraper with not_found_string for a simple dictionary with value (and date)
    Args:
        not_found_str (str): "Not found"
        value (dict): a dictionary with key "value" in the combined.json file
    """
    if "value" not in value.keys():
        return
    elif value["value"] == values.not_found or values.url_not_found == value["value"]:
        value["value"] = not_found_str


def add_condition(condition: dict, directory: str):
    """
    Adds attributes of the condition to the transformed.json corresponding to the condition's EU number
    Args:
        condition (dict): dictionary containing attributes of one condition of an OMAR
        directory (str): data folder, containing medicine folders
    """
    for folder in listdir(f"{directory}/active_withdrawn"):
        if condition["eu_od_number"].upper().replace('/', '-') != folder:
            continue
        med_path = f"{directory}/active_withdrawn/{folder}"
        transformed_file = [file for file in listdir(med_path) if path.isfile(path.join(med_path, file))
                            and "transformed.json" in file]

        if not transformed_file:
            continue

        transformed_json_path = f"{med_path}/{transformed_file[0]}"
        with open(transformed_json_path) as transformed_json:
            json_data = json.load(transformed_json)

        for key, value in condition.items():
            # Don't add EU number, as it's already present with capitals.
            if key == "eu_od_number":
                continue
            json_data[key] = value
            if value == values.not_found or value == values.url_not_found:
                json_data[key] = "Not found"
        save_transformed_json(transformed_json_path, json_data)


def add_orphan_con(eu_od_num: str, orphan_con: dict, directory: str):
    """
    Adds attributes of the condition to the transformed.json corresponding to the condition's EU number
    Args:
        eu_od_num (str): The orphan designation number of the relevant orphan
        orphan_con (dict): dictionary containing all orphan conditions for one orphan
        directory (str): data folder, containing medicine folders
    """
    for folder in listdir(f"{directory}/active_withdrawn"):
        if eu_od_num.upper().replace('/', '-') != folder:
            continue
        med_path = f"{directory}/active_withdrawn/{folder}"
        transformed_file = [file for file in listdir(med_path) if path.isfile(path.join(med_path, file))
                            and "transformed.json" in file]

        if not transformed_file:
            continue

        transformed_json_path = f"{med_path}/{transformed_file[0]}"
        with open(transformed_json_path) as transformed_json:
            json_data = json.load(transformed_json)
        json_data[attr.eu_orphan_con_current] = orphan_con

        save_transformed_json(transformed_json_path, json_data)


# Main file to run all parsers
def main(directory: str):
    """
    Given a folder containing medicine folders, converts each combined_attributes.json
    to the right format for the database.

    Args:
        directory (str): data folder, containing medicine folders
    """
    log.info(f"=== Transforming all combined_attributes.json files ===")

    # Get all combined.json files, and convert them to the right format
    for folder in listdir(f"{directory}/active_withdrawn"):
        med_path = f"{directory}/active_withdrawn/{folder}"
        combined_file = [file for file in listdir(med_path) if path.isfile(path.join(med_path, file))
                         and "combined.json" in file]
        if combined_file:
            combined_json_path = f"{med_path}/{combined_file[0]}"
            convert_json(combined_json_path)

    for condition in omar_conditions:
        add_condition(condition, directory)

    for eu_od_num in eu_orphan_con_currents:
        add_orphan_con(eu_od_num, eu_orphan_con_currents[eu_od_num], directory)

    log.info(f"=== Done transforming ===")


if __name__ == "__main__":
    main('../../../data')
