from unittest import TestCase, mock
from requests.exceptions import Timeout
from scraping.web_scraper import download


class TestDownload(TestCase):
    """
    Class that contains all the tests for scraping.webscraper.download
    """
    def test_download_pdf_from_url(self):
        download.download_pdf_from_url('', '', [])
        self.fail()

    def test_download_pdfs_ec(self):
        self.fail()

    def test_download_pdfs_ema(self):
        self.fail()

    def test_read_csv_files(self):
        self.fail()

    def test_download_medicine_files(self):
        self.fail()

    def test_download_all(self):
        self.fail()
