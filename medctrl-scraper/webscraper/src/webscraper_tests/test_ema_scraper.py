from unittest import TestCase
from ...src import ema_scraper


class TestEMAScraper(TestCase):
    def test_pdf_links_from_url(self):
        ema_scraper.pdf_links_from_url('')
        self.fail()


