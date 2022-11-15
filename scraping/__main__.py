import sys
import os.path as path
import os

import web_scraper.__main__ as web_scraper
import pdf_module.pdf_scraper.__main__ as pdf_scraper
import combiner.__main__ as combiner
import db_communicator.__main__ as db_communicator
import log_setup

scrape_ec: bool = True            # Whether EC URLs should be scraped
scrape_ema: bool = True           # Whether EMA URLs should be scraped | Requires scrape_ec to have been run once
download_files: bool = True       # Whether scraper should download PDFs from obtained links
run_filter: bool = True           # Whether filter should be run after downloading PDF files
use_parallelization: bool = True  # Whether downloading should be parallel (faster)


def main():
    """
    Runs the entire scraping process on the specified directory
    """
    data_folder_directory = '../data'
    # print(data_folder_directory)
    if not path.isdir(data_folder_directory):
        os.mkdir(data_folder_directory)

    # For now only the web_scraper and pdf_scraper will be run
    web_scraper.main(data_folder_directory, scrape_ec, scrape_ema, download_files, run_filter, use_parallelization)
    pdf_scraper.main(data_folder_directory)
    # combiner.main(data_folder_directory)
    # db_communicator_main.main(data_folder_directory)


if __name__ == '__main__':
    log_setup.init_loggers()
    main()
