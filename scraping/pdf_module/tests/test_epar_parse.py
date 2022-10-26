from unittest import TestCase
import regex as re
import sys
import os

from scraping.pdf_module.pdf_scraper.parsers import epar_parse
import xml.etree.ElementTree as ET

test_data_loc = "../../../data"
xml_bodies = []
percentage_str = "Percentage found: "


# Tests all functions of EPAR parser with all XML files
class TestEparParse(TestCase):
    def setUp(self):
        """
        Prepare a list of XML files in the global variable xml_bodies
        Returns:
            None
        """
        files = []
        for folder in os.listdir(test_data_loc):
            for file in os.listdir(os.path.join(test_data_loc, folder)):
                path = os.path.join(test_data_loc, folder, file)
                if os.path.isfile(path):
                    files.append(path)
        xml_files = [file for file in files if ".xml" in file and ("procedural-steps" in file or
                                                                   "public-assessment" in file)]

        # Get XML bodies, assuming there are XML files
        for xml_file in xml_files:
            xml_tree = ET.parse(xml_file)
            xml_root = xml_tree.getroot()
            xml_bodies.append(xml_root[1])

    def test_get_date(self):
        """
        Test getting ema_procedure_start_initial
        Returns:
            None
        """
        found_count = 0
        # Call get_date
        for xml_body in xml_bodies:
            output = epar_parse.get_date(xml_body)
            if output != "no_date_found":
                found_count += 1
                day = re.search(r"\d{2}/", output)[0][:2].strip()
                month = re.search(r"/\d{2}/", output)[0][1:3].strip()
                year = re.search(r"\d{4}", output)[0].strip()
                self.check_date(day, month, year)
        percentage_found = found_count / len(xml_bodies) * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        self.assertGreater(percentage_found, 90)

    def test_get_opinion_date(self):
        """
        Test getting chmp_opinion_date
        Returns:
            None
        """
        found_count = 0
        # Call get_opinion_date
        for xml_body in xml_bodies:
            output = epar_parse.get_opinion_date(xml_body)
            if output != "no_chmp_found":
                found_count += 1
                if not re.search(r"\d{2}/", output):
                    for i in xml_body.iter():
                        print(i.text)
                day = re.search(r"\d{2}/", output)[0][:2].strip()
                month = re.search(r"/\d{2}/", output)[0][1:3].strip()
                year = re.search(r"\d{4}", output)[0].strip()
                self.check_date(day, month, year)
        percentage_found = found_count / len(xml_bodies) * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        self.assertGreater(percentage_found, 90)

    def check_date(self, day: str, month: str, year: str):
        """
        Check for reasonable dates
        Args:
            day (str): day to check from scraped date
            month (str): month to check from scraped date
            year (str): year to check from scraped date

        Returns:
            None
        """
        self.assertGreater(int(year), 1980)
        # Make sure to check this in the future :D
        self.assertGreater(3000, int(year))
        self.assertGreater(int(month), 0)
        self.assertGreater(13, int(month))
        self.assertGreater(int(day), 0)
        self.assertGreater(32, int(day))

    def test_get_legal_basis(self):
        """
        Test getting eu_legal_basis
        Returns:
            None
        """
        found_count = 0
        # Call get_legal_basis
        for xml_body in xml_bodies:
            output = epar_parse.get_legal_basis(xml_body)
            if output != "no_legal_basis":
                found_count += 1
                self.assertGreater(len(output), 0)
                for article in output:
                    # Check if article is of correct format
                    article_number = re.search(r'article (\d|\.|[a-z])+', article)
                    self.assertIn("article", article)
                    self.assertTrue(article_number)
                    # There should not be any other characters in the output
                    other_chars = r"[^a-z|\d|\s|\.]"
                    self.assertFalse(re.search(other_chars, article))
        percentage_found = found_count / len(xml_bodies) * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        self.assertGreater(percentage_found, 90)

    def test_get_prime(self):
        """
        Test getting eu_prime_initial
        Returns:
            None
        """
        yes_exists = False
        # Call get_prime
        for xml_body in xml_bodies:
            output = epar_parse.get_prime(xml_body)
            if output == "yes":
                yes_exists = True
            self.assertIn(output, 'yesno')
        self.assertTrue(yes_exists)

    def test_get_rapp(self):
        """
        Test getting ema_rapp
        Returns:
            None
        """
        found_count = 0
        # Call get_rapp
        for xml_body in xml_bodies:
            output = epar_parse.get_rapp(xml_body)
            if not output:
                self.fail("Rapporteur is empty")
            if output != "no_rapporteur":
                print(output)
                found_count += 1
                # Check if rapporteur name is of reasonable length
                self.assertGreater(len(output), 2)
                self.assertGreater(40, len(output))
                # Check if rapporteur is of correct format
                rapp_format = re.search(r'[\w\s]+', output)
                self.assertTrue(rapp_format)
        percentage_found = found_count / len(xml_bodies) * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        self.assertGreater(percentage_found, 80)
