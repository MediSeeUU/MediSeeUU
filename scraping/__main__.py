import sys
import os.path as path
import os

import web_scraper
import pdf_scraper
import combiner
import db_uploader


def main():
    data_folder_directory = sys.argv[0]
    if not path.isdir(data_folder_directory):
        os.mkdir(data_folder_directory)

    web_scraper.main(data_folder_directory)
    pdf_scraper.main(data_folder_directory)
    combiner.main(data_folder_directory)
    db_uploader.main(data_folder_directory)
