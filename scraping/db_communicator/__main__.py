import json
from os import listdir, path
from db_communicator import DbCommunicator
import logging

log = logging.getLogger("db_communicator")


def main(directory: str):
    """
    Sends all combined data in the data folder to the database in separate requests

    Args:
        directory (string): The base directory containing all data
    """
    # Initialize the communicator class
    db_communicator = DbCommunicator()
    active_withdrawn_folder = path.join(directory, "active_withdrawn")

    directory_folders = [folder for folder in listdir(active_withdrawn_folder) if
                         path.isdir(path.join(active_withdrawn_folder, folder)) and "EU" in folder]

    medicine_no = 0
    for folder in directory_folders:
        combined_dict = communicator_folder(path.join(active_withdrawn_folder, folder), folder)
        if not combined_dict is None:
            json_data = json.dumps(combined_dict)
            db_communicator.send_data(data=json_data)
            medicine_no += 1
    log.info(str(medicine_no) + " medicines send to the database")

    # log the communicator out when finished
    db_communicator.logout()


def communicator_folder(cur_dir: str) -> dict:
    try:
        with open(path.join(cur_dir, "combined.json"), "r") as combined_json:
            return json.load(combined_json)
    except FileNotFoundError:
        print(f"COMMUNICATOR: no combined.json found in data for {cur_dir}")


if __name__ == '__main__':
    main()
