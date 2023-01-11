import json
import logging
from os import listdir, path

from db_communicator import DbCommunicator

log = logging.getLogger("db_communicator")


def main(directory: str, send_together=True):
    """
    Sends all transformed data in the data folder to the database in separate requests

    Args:
        directory (string): The base directory containing all data
        send_together (bool): Whether to send all medicine together in one file (True), or to send them individually
        (False)
    """
    # Initialize the communicator class
    try:
        db_communicator = DbCommunicator()
    except:
        log.error("Can't create a db_communicator instance. no medicines will be send to the database")
        return

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
    Iterates through all folders and sends the transformed data to the backend per medicine

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
        transformed_dict = get_transformed_dict(path.join(active_withdrawn_folder, folder), folder)
        if transformed_dict is not None:
            formed_data = {"data": [transformed_dict]}
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
    Iterates through all folders and sends the transformed data to the backend together in a singular file

    Args:
        directory_folders (list[str]): All folders to iterate through
        active_withdrawn_folder (str): The path to the active_withdrawn_folder
        db_communicator (DbCommunicator): An instance of the DbCommunicator
        medicine_type (str): A string describing the medicine type that are being sent. This is only used for logging
    """
    all_data = []

    for folder in directory_folders:
        transformed_dict = get_transformed_dict(path.join(active_withdrawn_folder, folder), folder)
        if transformed_dict is not None:
            all_data.append(transformed_dict)

    formed_data = {"data": all_data}
    json_data = json.dumps(formed_data)
    passed = db_communicator.send_data(data=json_data)

    if passed:
        log.info(f"Successfully sent all {medicine_type} medicines to the database")
    else:
        log.error(f"Couldn't send all {medicine_type} medicines to the database, is the backend running?")


def get_transformed_dict(cur_dir: str, med_name: str) -> dict | None:
    """
    tries to get the transformed json out of the current directory and convert it to dict

    Args:
        cur_dir (str): The directory string
        med_name (str): The name of the current medicine

    Returns:
        dict: The json file converted to a dictionary
    """
    try:
        with open(path.join(cur_dir, med_name + "_transformed.json"), "r", encoding='utf-8') as transformed_json:
            return json.load(transformed_json)
    except UnicodeDecodeError:
        with open(path.join(cur_dir, med_name + "_transformed.json", "r")) as transformed_json:
            return json.load(transformed_json)
    except FileNotFoundError:
        log.info(f"COMMUNICATOR: no transformed.json found in data for {cur_dir}")
        return
