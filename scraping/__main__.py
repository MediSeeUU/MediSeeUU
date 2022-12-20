from pathlib import Path
from datetime import datetime, timedelta

import pause

import scraping.web_scraper.__main__ as web_scraper
import scraping.xml_converter.__main__ as xml_converter
import scraping.pdf_parser.__main__ as pdf_parser
import scraping.annex_10_parser.__main__ as annex_10_parser
import scraping.combiner.__main__ as combiner
import scraping.db_communicator.__main__ as db_communicator
from scraping.utilities.log import log_tools
from scraping.utilities.web import config_objects
import scraping.utilities.debugging_tools.data_compiler as dc


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
    log_tools.init_loggers()
    data_folder_directory = create_data_folders()
    config_objects.default_path_data = data_folder_directory

    # Standard config is to run all. Uncomment line below to use custom setup.
    web_config = config_objects.WebConfig().run_all().set_parallel()
    # web_config = config_objects.WebConfig().run_custom(scrape_ec=True, scrape_ema=True).set_parallel()

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
    data_folder_dir = '../data'

    folders = [data_folder_dir + "/" + subdir
               for subdir in ["active_withdrawn", "refused", "annex_10"]]

    for folder in folders:
        Path(folder).mkdir(exist_ok=True, parents=True)

    return data_folder_dir


if __name__ == '__main__':
    run_all()  # TODO:  Replace this with "main()" when moved to server
    # main()
