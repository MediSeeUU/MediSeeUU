import sys
import os.path as path
import os

import web_scraper.__main__ as web_scraper
import pdf_module.pdf_scraper.__main__ as pdf_scraper
import combiner.__main__ as combiner
import db_communicator.__main__ as db_communicator_main


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

    web_scraper.main(data_folder_directory)
    pdf_scraper.main(data_folder_directory)


if __name__ == '__main__':
    main()
