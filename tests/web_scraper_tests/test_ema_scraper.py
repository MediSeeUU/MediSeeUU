import unittest
from datetime import datetime, date
from scraping.web_scraper import ema_scraper as em
import scraping.utilities.web.web_utils as utils
from parameterized import parameterized
import scraping.utilities.definitions.attributes as attr


class TestEMAScraper(unittest.TestCase):
    """
    Class that contains the tests for scraping.webscraper.ema_scraper
    """

    @parameterized.expand([
        [
            "EPAR and OMAR",
            "https://www.ema.europa.eu/en/medicines/human/EPAR/zynteglo",
            "https://www.ema.europa.eu/documents/assessment-report/zynteglo-epar-public-assessment-report_en.pdf",
            "https://www.ema.europa.eu/documents/orphan-maintenance-report/zynteglo-orphan-maintenance-assessment-"
            "report-initial-authorisation_en.pdf",
            ""
        ],
        [
            "EPAR only",
            "https://www.ema.europa.eu/en/medicines/human/EPAR/daklinza",
            "https://www.ema.europa.eu/documents/assessment-report/daklinza-epar-public-assessment-report_en.pdf",
            "",
            ""
        ],
        [
            "No EPAR and OMAR",
            "https://www.ema.europa.eu/en/medicines/human/orphan-designations/eu-3-21-2406",
            "",
            "",
            ""
        ],
        [
            "EPAR only",
            "https://www.ema.europa.eu/en/medicines/human/EPAR/alymsys",
            "https://www.ema.europa.eu/documents/assessment-report/alymsys-epar-public-assessment-report_en.pdf",
            "",
            ""
        ],
        [
            "ODWAR",
            "https://www.ema.europa.eu/en/medicines/human/EPAR/brukinsa",
            "https://www.ema.europa.eu/documents/assessment-report/brukinsa-epar-public-assessment-report_en.pdf",
            "",
            "https://www.ema.europa.eu/documents/orphan-maintenance-report/brukinsa-orphan-designation-withdrawal-"
            "assessment-report-initial-authorisation_en.pdf"
        ]
    ])
    def test_pdf_links_from_url(self, _, url: str, exp_epar: str, exp_omar: str, exp_odwar: str):
        """
        Checks whether the correct epar and omar urls are found.

        Args:
            _: Discard argument. Allows you to add a name to testcases in the `parameterized.expand`
            url (str): URL for the medicine to be checked.
            exp_epar (str): The expected epar file.
            exp_omar (str): The expected omar file.

        Returns:
            None: This function returns nothing.

        """
        html_active = utils.get_html_object(url)
        ema_links: dict = em.scrape_medicine_page(url, html_active)
        self.assertEqual(exp_epar, ema_links.get(attr.epar_url, ""), msg="epar is not correct")
        self.assertEqual(exp_omar, ema_links.get(attr.omar_url, ""), msg="omar is not correct")
        self.assertEqual(exp_odwar, ema_links.get(attr.odwar_url, ""), msg="odwar is not correct")

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
         datetime.strptime("15/12/2022", '%d/%m/%Y').date()]
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
