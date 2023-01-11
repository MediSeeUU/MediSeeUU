from datetime import datetime, timedelta
from pathlib import Path

import pause

import scraping.web_scraper.__main__ as web_scraper
import scraping.xml_converter.__main__ as xml_converter
import scraping.pdf_parser.__main__ as pdf_parser
import scraping.annex_10_parser.__main__ as annex_10_parser
import scraping.annex_comparer.__main__ as annex_comparer
import scraping.combiner.__main__ as combiner
import scraping.transformer.__main__ as transformer
import scraping.db_communicator.__main__ as db_communicator
import scraping.utilities.config.__main__ as cf
from scraping.utilities.log import log_tools
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
    log_tools.init_loggers()
    data_folder_directory = create_data_folders()
    config_objects.default_path_data = data_folder_directory

    # Standard config is to run all. Uncomment line below to use custom setup.
    web_config = config_objects.WebConfig().run_all().set_parallel()
    # web_config = config_objects.WebConfig().run_custom(scrape_ec=True, scrape_ema=True).set_parallel()

    # modules run based on configfile
    config = cf.load_config()
    if config[cf.run_web]:
        web_scraper.main(web_config)
    if config[cf.run_xml]:
        xml_converter.main(data_folder_directory, config[cf.xml_convert_all])
    if config[cf.run_pdf]:
        pdf_parser.main(data_folder_directory, config[cf.pdf_parse_all])
    if config[cf.run_annex_10]:
        annex_10_parser.main(data_folder_directory)
    if True:
        annex_comparer.main(data_folder_directory)
    if config[cf.run_combiner]:
        combiner.main(data_folder_directory)
    if config[cf.run_transformer]:
        transformer.main(data_folder_directory)
    if config[cf.run_db_com]:
        db_communicator.main(data_folder_directory, config[cf.db_com_send_together])


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
