from unittest import TestCase
import regex as re
import sys
import os
import scraping.file_parser.pdf_parser.helper as helper
import scraping.file_parser.xml_converter.xml_parsing_utils as xml_utils

from scraping.file_parser.pdf_parser.parsers import omar_parser
import xml.etree.ElementTree as ET

test_data_loc = "../../data"
xml_bodies = []

# Tests all functions of OMAR parser with all XML files
def xml_to_bullet_points(xml_body: ET.Element) -> list[str]:
    for section in xml_body:
        # scrape attributes specific to authorization annexes

        # Detect a condition
        if xml_utils.section_contains_header_substring_set_all(["comp", "adopted", "on"], section) \
                and not xml_utils.section_is_table_of_contents(section):
            section_string = xml_utils.section_append_paragraphs(section)
            return section_string.split("•")

    return []


class TestOmarParse(TestCase):
    """
    Class that contains the unit tests for scraping.file_parser.pdf_parser.scrapers.epar_parser
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
        xml_files = [file for file in files if "omar" in file and ".xml" in file]

        # Get XML bodies, assuming there are XML files
        for xml_file in xml_files:
            try:
                xml_tree = ET.parse(xml_file)
                xml_root = xml_tree.getroot()
                xml_body = xml_root[1]
                xml_bodies.append((xml_body, xml_file))
            except ET.ParseError:
                print("OMAR Test could not parse XML file " + xml_file)

        # Due to the significant changes to the OMAR parser, new unit tests have
        # to be written to accommodate this.

    def test_get_prevalence(self):
        """
        Test getting omar_alternative_treatments
        Returns:
            None
        """
        NAs_found = 0
        prevalence_found = 0

        for (xml_body, xml_file) in xml_bodies:
            bullet_point = xml_to_bullet_points(xml_body)
            result = omar_parse.get_prevalence(bullet_point)
            if result == "NA":
                NAs_found += 1
                print("No prevalence found in: " + xml_file)
            if "10.000" or "10,000" in result:
                prevalence_found += 1
            
        percentage_found = prevalence_found / (prevalence_found + NAs_found) * 100
        print("Prevalence found in " + str(round(percentage_found, 2)) + '%' +" of all files.")
        self.assertGreater(percentage_found, 90)


    def test_get_alternative_treatments(self):
        """
        Test getting omar_alternative_treatments
        Returns:
            None
        """

        self.assertTrue(True)

    def test_get_significant_benefit(self):

        self.assertTrue(True)
