import unittest
from datetime import datetime
from scraping.web_scraper import ema_scraper as em
import scraping.web_scraper.utils as utils
from parameterized import parameterized


class TestEMAScraper(unittest.TestCase):
    """
    Class that contains the tests for scraping.webscraper.ema_scraper
    """

    @parameterized.expand([
        [
            "https://www.ema.europa.eu/en/medicines/human/EPAR/zynteglo",
            "https://www.ema.europa.eu/documents/assessment-report/zynteglo-epar-public-assessment-report_en.pdf",
            "https://www.ema.europa.eu/documents/orphan-maintenance-report/zynteglo-orphan-maintenance-assessment-"
            "report-initial-authorisation_en.pdf"
        ],
        [
            "https://www.ema.europa.eu/en/medicines/human/EPAR/daklinza",
            "https://www.ema.europa.eu/documents/assessment-report/daklinza-epar-public-assessment-report_en.pdf",
            ""
        ],
        [
            "https://www.ema.europa.eu/en/medicines/human/orphan-designations/eu-3-21-2406",
            "",
            ""
        ],
        [
            "https://www.ema.europa.eu/en/medicines/human/EPAR/alymsys",
            "https://www.ema.europa.eu/documents/assessment-report/alymsys-epar-public-assessment-report_en.pdf",
            ""
        ]
    ])
    def test_pdf_links_from_url(self, url: str, exp_epar: str, exp_omar: str):
        """
        Checks whether the correct epar and omar urls are found.

        Args:
            url (str): URL for the medicine to be checked.
            exp_epar (str): The expected epar file.
            exp_omar (str): The expected omar file.

        Returns:
            None: This function returns nothing.

        """
        html_active = utils.get_html_object(url)
        epar, omar = em.pdf_links_from_url(url, html_active)
        self.assertEqual(exp_epar, epar, msg="epar is not correct")
        self.assertEqual(exp_omar, omar, msg="omar is not correct")

    @parameterized.expand([
        [
            ["first", "second", "third"],
            ["third", "second", "first"],
            "first"
        ],
        [
            ["first", "second", "third"],
            ["fourth", "fifth", "sixth"],
            ""
        ]
    ])
    def test_find_priority_link(self, priority_list: list[str], strings: list[str], exp_result):
        """
        Checks whether the correct priority links are found.

        Args:
            priority_list (list[str]): List of priority links.
            strings (list[str]): List of strings to be checked.
            exp_result (str): Expected link result.

        Returns:

        """
        result: str = em.find_priority_link(priority_list, strings)
        self.assertEqual(exp_result, result, msg="priority link was not found")

    @parameterized.expand([
        ["https://www.ema.europa.eu/en/medicines/human/EPAR/alymsys",
         datetime.strptime("06/07/2022", '%d/%m/%Y')]
    ])
    def test_find_last_updated_date(self, url, exp_output):
        """
        Checks whether the correct last updated date is found.

        Args:
            url (str): URL for the medicine to be checked.
            exp_output (str): Expected last updated date.
:

        Returns:
            None: This function returns nothing.
        """
        html_active = utils.get_html_object(url)
        output = em.find_last_updated_date(html_active)

        self.assertEqual(exp_output, output, msg="output is not as expected")

    """
    The function does not yet work well enough to have unit tests written for it
    def test_get_annex10_files(self):
    """
