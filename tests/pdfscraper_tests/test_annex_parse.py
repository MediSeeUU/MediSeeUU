from operator import contains
from unittest import TestCase
import os
import os.path as path
from xml.etree.ElementInclude import include
import regex as re
import fitz
import datetime
import json
import scraping.pdf_module.pdf_scraper.parsers.annex_parse as annex_parse
import scraping.pdf_module.pdf_scraper.__main__ as pdf_scraper

test_data_foldername = "test_annex_parse_data"

class TestAnnexParse(TestCase):
    def setUp(self) -> None:
        pdf_scraper.parse_folder(path.abspath(test_data_foldername), test_data_foldername)
        return super().setUp()


    def test_get_initial_type_of_eu_authorization(self):
        attributes_json = open(path.abspath(test_data_foldername) + "\\" + test_data_foldername + "_pdf_parser.json")
        annex_attributes = json.load(attributes_json)["annexes"]
        attributes_json.close()

        all_in_correct_files = True
        all_correct_value = True

        for file_attributes in annex_attributes:
            pdf_file = file_attributes["pdf_file"]
            contains_attribute = "initial_type_of_eu_authorization" in file_attributes.keys()
            authorization_type = ""
            if contains_attribute:
                authorization_type = file_attributes["initial_type_of_eu_authorization"]

            in_correct_file = True
            correct_value = True

            # test whether attributes are in the right files
            if not file_attributes["is_initial"] and contains_attribute:
                in_correct_file = False
            
            if file_attributes["is_initial"] and not contains_attribute:
                in_correct_file = False

            # test for attribute values
            if file_attributes["is_initial"]:
                if "conditional approval" in pdf_file and authorization_type != "conditional":
                    correct_value = False

                if "specific obligation" in pdf_file and authorization_type != "exceptional or conditional":
                    correct_value = False

                if "specific obligations" in pdf_file and authorization_type != "exceptional or conditional":
                    correct_value = False

                if "standard approval" in pdf_file and authorization_type != "standard":
                    correct_value = False

            if not in_correct_file:
                print("TEST ERROR: " + str(pdf_file) + " initial_type_of_eu_authorization not in correct file: " + contains_attribute)
        
            if not correct_value:
                print("TEST ERROR: " + str(pdf_file) + " contains incorrect initial_type_of_eu_authorization: " + str(authorization_type))

            all_in_correct_files &= in_correct_file
            all_correct_value &= correct_value

        assert(all_in_correct_files and all_correct_value)


    def test_get_eu_type_of_medicine(self):
        return


