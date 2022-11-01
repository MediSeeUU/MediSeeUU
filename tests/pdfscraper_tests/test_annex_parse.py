from unittest import TestCase
import os
import regex as re
import fitz
import datetime
<<<<<<< Updated upstream
import scraping.pdf_module.pdf_scraper.parsers.annex_parse as annex_parser
=======
import scraping.pdf_module.pdf_scraper.parsers.annex_parser as annex_parser
import scraping.pdf_module.pdf_scraper.__main__ as pdf_scraper
>>>>>>> Stashed changes

test_data_foldername = "test_annex_parse_data"

class TestAnnexParse(TestCase):
    def setUp(self) -> None:
        pdf_scraper.parse_folder(os.path.abspath(test_data_foldername), test_data_foldername)
        return super().setUp()

    def test_get_initial_type_of_eu_authorization(self):
        allAuthorizationTypesCorrect = True

        return

    def test_get_eu_type_of_medicine(self):
        return


