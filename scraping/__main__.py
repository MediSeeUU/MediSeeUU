import os.path as path
import os
import pause
from datetime import datetime, timedelta

import web_scraper.__main__ as web_scraper
import scraping.annex_10_parser.__main__ as annex_10_parser
import scraping.xml_converter.__main__ as xml_converter
import scraping.pdf_parser.__main__ as pdf_parser
from scraping.utilities.log import log_tools
from scraping.utilities.io import safe_io
from scraping.utilities.web import config_objects


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
    # Creates the data directory if it does not exist
    data_folder_directory = create_data_folders()

    # Standard config is to run all. Uncomment line below to use custom setup.
    web_config = config_objects.WebConfig().run_all().set_parallel()
    # web_config = config_objects.WebConfig().run_custom(download_ema_excel=True).set_parallel()

    # Any module can be commented or uncommented here, as the modules they work separately
    web_scraper.main(web_config)
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
    data_folder_active_withdrawn = f"{data_folder_directory}/active_withdrawn"
    data_folder_refused_directory = f"{data_folder_directory}/refused"
    data_folder_annex10_directory = f"{data_folder_directory}/annex_10"
    folders = [data_folder_directory, data_folder_active_withdrawn, data_folder_refused_directory,
               data_folder_annex10_directory]

    for folder in folders:
        safe_io.create_folder(folder)

    return data_folder_directory


if __name__ == '__main__':
    log_tools.init_loggers()
    run_all()  # TODO:  Replace this with "main()" when moved to server
    # main()
