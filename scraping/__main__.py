import os.path as path
import os
import pause
from datetime import datetime, timedelta

import web_scraper.__main__ as web_scraper
import file_parser.pdf_parser.__main__ as pdf_parser
import file_parser.xml_converter.__main__ as xml_converter
import combiner.__main__ as combiner
import db_communicator.__main__ as db_communicator


def main():
    """
    Runs the entire scraping process on the specified directory every week
    """
    run = True
    while run:
        start_time = datetime.now()
        run_all()
        run = False
        pause.until(start_time + timedelta(days=7))  # Wait for seven days until the next scrape cycle


def run_all():
    """
    Runs all modules of MediSee
    For now only the web_scraper and pdf_parser will be run.
    """
    data_folder_directory = '../data'
    if not path.isdir(data_folder_directory):
        os.mkdir(data_folder_directory)

    # web_scraper.main(data_folder_directory)
    # xml_converter.main(data_folder_directory)
    pdf_parser.main(data_folder_directory)
    # combiner.main(data_folder_directory)
    # db_communicator_main.main(data_folder_directory)


if __name__ == '__main__':
    run_all()  # TODO:  Replace this with "main()" when moved to server
    # main()
