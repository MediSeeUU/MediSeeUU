from unittest import TestCase
from scraping.web_scraper import ema_scraper


class TestEMAScraper(TestCase):
    """
    Class that contains the tests for scraping.webscraper.ema_scraper
    """
    def test_pdf_links_from_url(self):
        ema_scraper.pdf_links_from_url('')
        self.fail()



