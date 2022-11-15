from unittest import TestCase
import regex as re
import sys
import os
import scraping.file_parser.pdf_parser.helper as helper

from scraping.file_parser.pdf_parser.parsers import epar_parser
import xml.etree.ElementTree as ET


test_data_loc = "../../data"
xml_bodies = []
percentage_str = "Percentage found: "


# Tests all functions of EPAR parser with all XML files
class TestEparParse(TestCase):
    """
    Class that contains the unit tests for scraping.file_parser.pdf_parser.scrapers.epar_parser
    """
    @classmethod
    def setUpClass(cls):
        """
        Prepare a list of XML files in the global variable xml_bodies
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
            try:
                xml_tree = ET.parse(xml_file)
                xml_root = xml_tree.getroot()
                xml_bodies.append((xml_root[1], xml_file))
            except ET.ParseError:
                print("EPAR Test could not parse XML file " + xml_file)

    def test_get_date(self):
        """
        Test getting ema_procedure_start_initial
        """
        found_count = 0
        # Call get_date
        for (xml_body, filename) in xml_bodies:
            output = epar_parser.get_date(xml_body)
            if output != "no_date_found" and output != "not_easily_scrapable":
                found_count += 1
                day = re.search(r"\d{2}/", output)[0][:2].strip()
                month = re.search(r"/\d{2}/", output)[0][1:3].strip()
                year = re.search(r"\d{4}", output)[0].strip()
                self.check_date(day, month, year)
            elif output == "not_easily_scrapable":
                print("Found but not scrapable: " + filename)
        percentage_found = found_count / len(xml_bodies) * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        self.assertGreater(percentage_found, 98)

    def test_get_opinion_date(self):
        """
        Test getting chmp_opinion_date
        """
        found_count = 0
        # Call get_opinion_date
        for (xml_body, filename) in xml_bodies:
            output = epar_parser.get_opinion_date(xml_body)
            if output != "no_chmp_found" and output != "not_easily_scrapable":
                found_count += 1
                day = re.search(r"\d{2}/", output)[0][:2].strip()
                month = re.search(r"/\d{2}/", output)[0][1:3].strip()
                year = re.search(r"\d{4}", output)[0].strip()
                self.check_date(day, month, year)
            elif output == "not_easily_scrapable":
                print("Found but not scrapable: " + filename)
        percentage_found = found_count / len(xml_bodies) * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        self.assertGreater(percentage_found, 98)

    def check_date(self, day: str, month: str, year: str):
        """
        Check for reasonable dates
        Args:
            day (str): day to check from scraped date
            month (str): month to check from scraped date
            year (str): year to check from scraped date
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
        """
        found_count = 0
        # Call get_legal_basis
        for (xml_body, filename) in xml_bodies:
            output = epar_parser.get_legal_basis(xml_body)
            if output != ["no_legal_basis"] and output != ["not_easily_scrapable"]:
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
                    # The article should be in the list of legal bases
                    if article not in helper.legal_bases:
                        print(f"Legal basis {article} not in list for file {filename}")
            elif output == ["not_easily_scrapable"]:
                print("Found but not scrapable: " + filename)
        percentage_found = found_count / len(xml_bodies) * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        self.assertGreater(percentage_found, 97)

    def test_get_prime(self):
        """
        Test getting eu_prime_initial
        """
        yes_exists = False
        na_exists = False
        # Call get_prime
        for (xml_body, filename) in xml_bodies:
            output = epar_parser.get_prime(xml_body)
            if output == "yes":
                yes_exists = True
            if output == "NA":
                na_exists = True
            self.assertIn(output, 'yesnoNA')
        self.assertTrue(yes_exists)
        self.assertTrue(na_exists)

    def test_get_rapp(self):
        """
        Test getting ema_rapp
        """
        found_count = 0
        # Call get_rapp
        for (xml_body, filename) in xml_bodies:
            output = epar_parser.get_rapp(xml_body)
            if not output:
                self.fail("Rapporteur is empty")
            # No rapporteur present in file, do not count as not scraped
            elif output == "no_rapporteur":
                found_count += 1
            elif output != "no_rapporteur" and output != "not_easily_scrapable":
                found_count += 1
                # Check if rapporteur name is of reasonable length
                self.assertGreater(len(output), 2)
                self.assertGreater(38, len(output))
                self.assertNotIn("\n", output)
                # Check if rapporteur is of correct format
                rapp_format = re.search(r'[\w\s]+', output)
                self.assertTrue(rapp_format)
            elif output == "not_easily_scrapable":
                print("Found but not scrapable: " + filename)
        percentage_found = found_count / len(xml_bodies) * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        self.assertGreater(percentage_found, 97)

    def test_get_corapp(self):
        """
        Test getting ema_corapp
        """
        found_count = 0
        # Call get_corapp
        for (xml_body, filename) in xml_bodies:
            output = epar_parser.get_corapp(xml_body)
            if not output:
                self.fail("Co-rapporteur is empty")
            # No rapporteur present in file, do not count as not scraped
            elif output == "no_co-rapporteur":
                found_count += 1
            elif output != "not_easily_scrapable":
                found_count += 1
                # Check if co-rapporteur name is of reasonable length
                self.assertGreater(len(output), 2)
                self.assertGreater(40, len(output))
                self.assertNotIn("\n", output)
                # Check if rapporteur is of correct format
                rapp_format = re.search(r'[\w\s]+', output)
                self.assertTrue(rapp_format)
            elif output == "not_easily_scrapable":
                print("Found but not scrapable: " + filename)
        percentage_found = found_count / len(xml_bodies) * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        # There aren't a lot of co-rapporteurs, just to make sure the function keeps working correctly
        self.assertGreater(percentage_found, 98)

    def test_get_reexamination(self):
        """
        Test getting ema_reexamination
        """
        yes_exists = False
        # Call get_reexamination
        for (xml_body, filename) in xml_bodies:
            output = epar_parser.get_reexamination(xml_body)
            if output == "yes":
                yes_exists = True
            if not output:
                self.fail("No output found")
            self.assertIn(output, 'yesno')
        self.assertTrue(yes_exists)

    def test_get_accelerated_assessment(self):
        """
        Test getting eu_accel_assess_g
        """
        yes_exists = False
        # Call get_accelerated_assessment
        for (xml_body, filename) in xml_bodies:
            output = epar_parser.get_accelerated_assessment(xml_body)
            if output == "yes":
                yes_exists = True
            if not output:
                self.fail("No output found")
            self.assertIn(output, 'yesnoNA')
        self.assertTrue(yes_exists)
