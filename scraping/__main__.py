import sys
import os.path as path
import os

<<<<<<< Updated upstream
import web_scraper.__main__ as web_scraper
import pdf_module.pdf_scraper.__main__ as pdf_scraper
import combiner.__main__ as combiner
<<<<<<< Updated upstream
from db_communicator import DbCommunicator
import db_communicator.__main__ as db_communicator_main

# Create static db_communicator
db_communicator = DbCommunicator()
=======
import db_uploader.__main__ as db_uploader
=======
# import web_scraper.__main__ as web_scraper
# import pdf_module.pdf_scraper.__main__ as pdf_scraper
# import combiner.__main__ as combiner
from db_communicator import DbCommunicator
import db_communicator.__main__ as db_communicator_main

# Import the key when using the db_communicator
# POSSIBLE ERROR: the api key could be overwritten every import
api_key = ''
db_communicator = DbCommunicator()
>>>>>>> Stashed changes
>>>>>>> Stashed changes


def main():
    """
    Runs the entire scraping process on the specified directory
    Returns:
        None
    """
    data_folder_directory = '../data'
    # print(data_folder_directory)
    if not path.isdir(data_folder_directory):
        os.mkdir(data_folder_directory)

    ## NOTE: Uncomment any of the following modules to run the module
    # web_scraper.main(data_folder_directory)
    # pdf_scraper.main(data_folder_directory)
    # combiner.main(data_folder_directory)
    db_communicator_main.main(data_folder_directory)


if __name__ == '__main__':
    main()
