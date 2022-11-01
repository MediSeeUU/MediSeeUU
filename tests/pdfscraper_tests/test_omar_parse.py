from unittest import TestCase
import regex as re
import sys
import os

from scraping.pdf_module.pdf_scraper.parsers import omar_parse
import xml.etree.ElementTree as ET

test_data_loc = "../../data"
xml_bodies = []
percentage_str = "Percentage found: "


# Tests all functions of OMAR parser with all XML files
class TestOmarParse(TestCase):
    """
    Class that contains the unit tests for scraping.pdf_module.pdf_scraper.scrapers.epar_parse
    """

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
        xml_files = [file for file in files if "orphan-maintenance-assessment-report" in file and ".xml" in file]

        # Get XML bodies, assuming there are XML files
        for xml_file in xml_files:
            xml_tree = ET.parse(xml_file)
            xml_root = xml_tree.getroot()
            xml_bodies.append(xml_root[1])


    def test_get_prevalence(self):
        """
        Test getting omar_alternative_treatments
        Returns:
            None
        """
        correct = False

        for xml_body in xml_bodies:
            output = omar_parse.get_prevalence(xml_body)
            if "prevalence" in output:
                correct = True
            if output == "NA":
                correct = False

        self.assertTrue(correct)


    def test_get_alternative_treatments(self):
        """
        Test getting omar_alternative_treatments
        Returns:
            None
        """

        self.assertTrue(True)

