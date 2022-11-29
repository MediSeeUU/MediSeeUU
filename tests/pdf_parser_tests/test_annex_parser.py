from unittest import TestCase
import os
import os.path as path
import json
import scraping.pdf_parser.__main__ as pdf_parser
import scraping.utilities.definitions.attributes as attr
import scraping.utilities.definitions.value as values

test_data_folder_path = "pdf_parser_tests/test_annex_parse_data"
if "pdf_parser_tests" in os.getcwd():
    test_data_folder_path = "test_annex_parse_data"
test_data_folder_name = "test_annex_parse_data"


class TestAnnexParse(TestCase):
    """
    Unit testing annex_parser attribute scraping correctness with handmade test PDF files.

    Tested attributes:
        - eu_type_of_medicine
        - initial_type_of_eu_authorization
    """
    annex_attributes: dict[str, str]

    def setUp(self):
        """
        Sets up the xml files from test pdf's and then scrapes data from them into a json and reads it so other
        functions can use the data. Automatically run when whoe test class is used.
        """
        pdf_parser.parse_folder(path.abspath(test_data_folder_path), test_data_folder_name)
        # TODO: Try/catch this with appropriate exception when file does not exist
        attributes_json = open(
            path.join(path.abspath(test_data_folder_path), test_data_folder_name + "_pdf_parser.json"))
        self.annex_attributes = json.load(attributes_json)["annexes"]
        attributes_json.close()
        return super().setUp()

    def test_get_initial_type_of_eu_authorization(self):
        """
        Unit test for scraping initial_type_of_eu_authorization attribute. This test checks whether this attribute is
        only read in initial authorization annex files and whether the value is correct and found in all applicable
        cases.
        """
        incorrect_files = False
        incorrect_values = False

        for file_attributes in self.annex_attributes:
            # setup file check
            pdf_file = file_attributes[attr.pdf_file]
            contains_attribute = attr.eu_aut_type_initial in file_attributes.keys()
            authorization_type = ""
            if contains_attribute:
                authorization_type = file_attributes[attr.eu_aut_type_initial]

            incorrect_file = False
            incorrect_value = False

            # test whether attributes are in the right files
            incorrect_file |= not (file_attributes[attr.is_initial] == contains_attribute)

            # test for attribute values
            if file_attributes[attr.is_initial]:
                incorrect_value |= "specific obligation" in pdf_file and authorization_type != values.authorization_type_unknown
                incorrect_value |= "specific obligations" in pdf_file and authorization_type != values.authorization_type_unknown
                incorrect_value |= "conditional approval" in pdf_file and authorization_type != values.aut_type_conditional
                incorrect_value |= "standard approval" in pdf_file and authorization_type != values.aut_type_standard

            # print errors
            if incorrect_file:
                print("\nTEST ERROR: " + str(
                    pdf_file) + "  incorrect presence of initial_type_of_eu_authorization | presence " +
                      str(contains_attribute))

            if incorrect_value:
                print("\nTEST ERROR: " + str(pdf_file) + " contains incorrect initial_type_of_eu_authorization: " +
                      str(authorization_type))

            incorrect_files |= incorrect_file
            incorrect_values |= incorrect_value

        assert (not incorrect_files and not incorrect_values)

    def test_get_eu_type_of_medicine(self):
        """
        Unit test for scraping eu_type_of_medicine attribute. This test checks whether this attribute is only read in
        initial authorization annex files and whether the value is correct and found in all applicable cases.
        """
        incorrect_files = False
        incorrect_values = False

        for file_attributes in self.annex_attributes:
            # setup file check
            pdf_file = file_attributes[attr.pdf_file]
            contains_attribute = attr.eu_med_type in file_attributes.keys()
            medicine_type = ""
            if contains_attribute:
                medicine_type = file_attributes[attr.eu_med_type]

            incorrect_file = False
            incorrect_value = False

            # test whether attributes are in the right files
            incorrect_file |= not (file_attributes[attr.is_initial] == contains_attribute)

            # test for attribute values
            if file_attributes[attr.is_initial]:
                incorrect_value |= values.eu_med_type_small_molecule in pdf_file and medicine_type != values.eu_med_type_small_molecule
                incorrect_value |= "biologicals header" in pdf_file and medicine_type not in [values.eu_med_type_biologicals, values.eu_med_type_atmp]

            # print errors
            if incorrect_file:
                print("\nTEST ERROR: " + str(
                    pdf_file) + " incorrect presence of eu_type_of_medicine | presence: " + str(contains_attribute))

            if incorrect_value:
                print(
                    "\nTEST ERROR: " + str(pdf_file) + " contains incorrect eu_type_of_medicine: " + str(medicine_type))

            incorrect_files |= incorrect_file
            incorrect_values |= incorrect_value

        assert (not incorrect_files and not incorrect_values)
