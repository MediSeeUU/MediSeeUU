import logging
from os import listdir, path
import json

log = logging.getLogger("combiner.transformer")

# TODO: change_date moeten echt een date/datetime zijn (filter alle histories eruit die dit niet zijn)
# TODO: orphan attributen in orphan json (omar_url, ema_omar_condition)


def convert_json(combined_json_path: str):
    """
    Converts one JSON to the right format for the database
    Args:
        combined_json_path (str): Path to the JSON file
    """
    with open(combined_json_path) as combined_json:
        json_data = json.load(combined_json)
        print(json_data)


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
        break

    log.info(f"=== Done transforming ===")


if __name__ == "__main__":
    main('../../../data')
