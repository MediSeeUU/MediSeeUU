import os.path as path
import os
import pause
from datetime import datetime, timedelta

import web_scraper.__main__ as web_scraper
import file_parser.annex_10_parser.__main__ as annex_10_parser
import file_parser.xml_converter.__main__ as xml_converter
import file_parser.pdf_parser.__main__ as pdf_parser
import combiner.__main__ as combiner
import db_communicator.__main__ as db_communicator
import log_setup


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
    scrape_ec: bool = False            # Whether EC URLs should be scraped
    scrape_ema: bool = False           # Whether EMA URLs should be scraped | Requires scrape_ec to have been run once
    download_files: bool = True       # Whether scraper should download PDFs from obtained links
    download_refused_files = True     # Whether scraper should download refused PDFs from obtained links
    run_filter: bool = False           # Whether filter should be run after downloading PDF files
    download_annex10_files = True     # Whether scraper should download annex10 files from obtained links
    use_parallelization: bool = True  # Whether downloading should be parallel (faster)

    # Creates the data directory if it does not exist
    data_folder_directory = create_data_folders()

    # Any module can be commented or uncommented here, as the modules they work separately
    web_scraper.main(data_folder_directory, scrape_ec, scrape_ema, download_files, download_refused_files,
                     download_annex10_files, run_filter, use_parallelization)
    xml_converter.main(data_folder_directory)
    pdf_parser.main(data_folder_directory)
    annex_10_parser.main(data_folder_directory)
    # combiner.main(data_folder_directory)
    # db_communicator_main.main(data_folder_directory)


def create_data_folders() -> str:
    """
    Creates the necessary data folders if they don't exist.

    Returns:
        str: Returns the data folder directory.

    """
    data_folder_directory = '../data'
    data_folder_active_withdrawn = data_folder_directory + "/active_withdrawn"
    data_folder_refused_directory = data_folder_directory + "/refused"
    data_folder_annex10_directory = data_folder_directory + "/annex_10"
    folders = [data_folder_directory, data_folder_active_withdrawn, data_folder_refused_directory,
               data_folder_annex10_directory]

    for folder in folders:
        if not path.isdir(folder):
            os.mkdir(folder)

    return data_folder_directory


if __name__ == '__main__':
    log_setup.init_loggers()
    run_all()  # TODO:  Replace this with "main()" when moved to server
    # main()
