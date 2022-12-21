import json
from os import listdir, path
from db_communicator import DbCommunicator
import logging

log = logging.getLogger("db_communicator")


def main(directory: str, send_together=True):
    """
    Sends all combined data in the data folder to the database in separate requests

    Args:
        directory (string): The base directory containing all data
        send_together (bool): Whether to send all medicine together in one file (True), or to send them individually
        (False)
    """
    # Initialize the communicator class
    db_communicator = DbCommunicator()

    active_withdrawn_folder = path.join(directory, "active_withdrawn")
    directory_human_folders = [folder for folder in listdir(active_withdrawn_folder) if
                               path.isdir(path.join(active_withdrawn_folder, folder)) and "EU-1" in folder]

    directory_orphan_folders = [folder for folder in listdir(active_withdrawn_folder) if
                                path.isdir(path.join(active_withdrawn_folder, folder)) and "EU-3" in folder]

    if send_together:
        send_medicine_together(directory_human_folders, active_withdrawn_folder, db_communicator, "human", )
        send_medicine_together(directory_orphan_folders, active_withdrawn_folder, db_communicator, "orphan")
    else:
        send_medicine(directory_human_folders, active_withdrawn_folder, db_communicator, "human", )
        send_medicine(directory_orphan_folders, active_withdrawn_folder, db_communicator, "orphan")

    # log the communicator out when finished
    db_communicator.logout()


def send_medicine(directory_folders: list[str], active_withdrawn_folder: str, db_communicator: DbCommunicator,
                  medicine_type="generic"):
    """
    Iterates through all folders and sends the combined data to the backend per medicine

    Args:
        directory_folders (list[str]): All folders to iterate through
        active_withdrawn_folder (str): The path to the active_withdrawn_folder
        db_communicator (DbCommunicator): An instance of the DbCommunicator
        medicine_type (str): A string describing the medicine type that are being sent. This is only used for logging
    """
    # Logger variables
    medicine_no = 0
    passed_medicine = 0
    failed_medicine = 0

    for folder in directory_folders:
        combined_dict = get_combined_dict(path.join(active_withdrawn_folder, folder), folder)
        if combined_dict is not None:
            formed_data = {"data": [combined_dict]}
            json_data = json.dumps(formed_data)
            passed = db_communicator.send_data(data=json_data)
            medicine_no += 1
            if passed:
                passed_medicine += 1
            else:
                failed_medicine += 1

    log.info(
        f"Tried to send {medicine_no} {medicine_type} medicines to the database. {passed_medicine} medicines "
        f"succeeded | {failed_medicine} medicines failed")


def send_medicine_together(directory_folders: list[str], active_withdrawn_folder: str, db_communicator: DbCommunicator,
                           medicine_type="generic"):
    """
    Iterates through all folders and sends the combined data to the backend together in a singular file

    Args:
        directory_folders (list[str]): All folders to iterate through
        active_withdrawn_folder (str): The path to the active_withdrawn_folder
        db_communicator (DbCommunicator): An instance of the DbCommunicator
        medicine_type (str): A string describing the medicine type that are being sent. This is only used for logging
    """
    all_data = []

    for folder in directory_folders:
        combined_dict = get_combined_dict(path.join(active_withdrawn_folder, folder), folder)
        if combined_dict is not None:
            all_data.append(combined_dict)

    formed_data = {"data": all_data}
    json_data = json.dumps(formed_data)
    print(json_data)
    passed = db_communicator.send_data(data=json_data)

    if passed:
        log.info(f"Successfully sent all {medicine_type} medicines to the database")
    else:
        log.error(f"Couldn't send all {medicine_type} medicines to the database, is the backend running?")


def get_combined_dict(cur_dir: str, med_name: str) -> dict | None:
    """
    tries to get the combined json out of the current directory

    Args:
        cur_dir (str): The directory string
        med_name (str): The name of the current medicine

    Returns:
        dict: The dictionary inside the json file
    """
    try:
        with open(path.join(cur_dir, med_name + "_combined.json"), "r") as combined_json:
            return json.load(combined_json)
    except FileNotFoundError:
        log.info(f"COMMUNICATOR: no combined.json found in data for {cur_dir}")
        return None
