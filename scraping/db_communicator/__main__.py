import json
import os
import time

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
    # db_communicator.logout_communicator()
    db_communicator.logout()
    # medicine_no = 0
    # for medicine_dir in os.listdir(directory):
    #     full_medicine_dir = os.path.join(directory, medicine_dir)
    #     for file in os.listdir(full_medicine_dir):
    #         if file.endswith("combined.json"):
    #             full_combined_dir = os.path.join(full_medicine_dir, file)
    #             with open(full_combined_dir, "r") as file_data:
    #                 json_string = json.load(file_data)
    #                 json_data = json.dumps(json_string)
    #                 db_communicator.send_data(data=json_data)
    #                 medicine_no += 1
    # log.info(str(medicine_no) + " medicines send to the database")


if __name__ == '__main__':
    main()
