from operator import contains
from unittest import TestCase
import os.path as path
from xml.etree.ElementInclude import include
import regex as re
import json
import scraping.pdf_module.pdf_scraper.__main__ as pdf_scraper

test_data_foldername = "test_annex_parse_data"


class TestAnnexParse(TestCase):
    """
    Unit testing annex_parse attribute scraping correctness with handmade test PDF files.
    Tested attributes:
        eu_type_of_medicine
        initial_type_of_eu_authorization
    """
    annex_attributes: dict[str, str]

    def setUp(self) -> None:
        """
        Sets up the xml files from test pdf's and then scrapes data from them into a json and reads it so other functions can use the data.
        Automatically run when whoe test class is used.

        Returns:
            None
        """        
        pdf_scraper.parse_folder(path.abspath(test_data_foldername), test_data_foldername)
        attributes_json = open(path.join(path.abspath(test_data_foldername), test_data_foldername + "_pdf_parser.json"))

        self.annex_attributes = json.load(attributes_json)["annexes"]
        attributes_json.close()
        return super().setUp()

    def test_get_initial_type_of_eu_authorization(self):
        """
        Unit test for scraping initial_type_of_eu_authorization attribute.
        This test checks whether this attribute is only read in initial authorization annex files and whether the value is correct and found in all applicable cases.

        Returns:
            None
        """        
        incorrect_files = False
        incorrect_values = False

        for file_attributes in self.annex_attributes:
            # setup file check
            pdf_file = file_attributes["pdf_file"]
            contains_attribute = "initial_type_of_eu_authorization" in file_attributes.keys()
            authorization_type = ""
            if contains_attribute:
                authorization_type = file_attributes["initial_type_of_eu_authorization"]

            incorrect_file = False
            incorrect_value = False

            # test whether attributes are in the right files
            incorrect_file |= not (file_attributes["is_initial"] == contains_attribute)

            # test for attribute values
            if file_attributes["is_initial"]:
                incorrect_value |= "specific obligation" in pdf_file and authorization_type != "exceptional or conditional"
                incorrect_value |= "specific obligations" in pdf_file and authorization_type != "exceptional or conditional"
                incorrect_value |= "conditional approval" in pdf_file and authorization_type != "conditional"
                incorrect_value |= "standard approval" in pdf_file and authorization_type != "standard"

            # print errors
            if incorrect_file:
                print("\nTEST ERROR: " + str(
                    pdf_file) + "  incorrect presence of initial_type_of_eu_authorization | presence " + contains_attribute)

            if incorrect_value:
                print("\nTEST ERROR: " + str(pdf_file) + " contains incorrect initial_type_of_eu_authorization: " + str(
                    authorization_type))

            incorrect_files |= incorrect_file
            incorrect_values |= incorrect_value

        assert (not incorrect_files and not incorrect_values)

    def test_get_eu_type_of_medicine(self):
        """
        Unit test for scraping eu_type_of_medicine attribute.
        This test checks whether this attribute is only read in initial authorization annex files and whether the value is correct and found in all applicable cases.

        Returns:
            None
        """      
        incorrect_files = False
        incorrect_values = False

        for file_attributes in self.annex_attributes:
            # setup file check
            pdf_file = file_attributes["pdf_file"]
            contains_attribute = "eu_type_of_medicine" in file_attributes.keys()
            medicine_type = ""
            if contains_attribute:
                medicine_type = file_attributes["eu_type_of_medicine"]

            incorrect_file = False
            incorrect_value = False

            # test whether attributes are in the right files
            incorrect_file |= not (file_attributes["is_initial"] == contains_attribute)

            # test for attribute values
            if file_attributes["is_initial"]:
                incorrect_value |= "small molecule" in pdf_file and medicine_type != "small molecule"
                incorrect_value |= "biologicals" in pdf_file and medicine_type != "biologicals"

            # print errors
            if incorrect_file:
                print("\nTEST ERROR: " + str(
                    pdf_file) + " incorrect presence of eu_type_of_medicine | presence: " + contains_attribute)

            if incorrect_value:
                print(
                    "\nTEST ERROR: " + str(pdf_file) + " contains incorrect eu_type_of_medicine: " + str(medicine_type))

            incorrect_files |= incorrect_file
            incorrect_values |= incorrect_value

        assert (not incorrect_files and not incorrect_values)