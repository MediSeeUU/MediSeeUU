from unittest import TestCase
from scraping.annex_10_parser import __main__ as annex_10_parser
import json
import os
import pandas as pd
import scraping.utilities.definitions.attributes as attr

data_loc = "../test_data"
if "annex_10_tests" in os.getcwd():
    data_loc = "../../test_data"
annex_10_data = {}


def clean_df(excel_data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the Excel file by removing null lines, starting rows from first Product Name value,
    naming the columns, and removing other columns than the last two

    Args:
        excel_data (pd.DataFrame): the contents of the Excel file

    Returns:
        pd.DataFrame: the cleaned contents of the Excel file
    """
    # Clean null lines
    excel_data = excel_data[~excel_data["Unnamed: 0"].isnull()]
    # Remove all rows before "Product Name"
    x = excel_data.index[excel_data["Unnamed: 0"] == "Product Name"].tolist()[0]
    excel_data = excel_data.truncate(before=x).reset_index()
    # Set column names
    excel_data.columns = excel_data.iloc[0]
    excel_data = excel_data.truncate(before=1).reset_index()
    # Remove redundant columns, only the last two columns contain the clock times we need.
    excel_data = excel_data.iloc[:, 2:]

    return excel_data


class TestAnnex10Parser(TestCase):
    """
    Class to test annex_10_parser using integration tests.
    """

    @classmethod
    def setUpClass(cls):
        """
        Run annex 10 parser
        """
        annex_10_parser.main(data_loc)
        parser_json_path = "annex_10_tests/annex_10_parser_test.json"
        if "annex_10_tests" in os.getcwd():
            parser_json_path = "annex_10_parser_test.json"
        file = open(parser_json_path, "r")
        global annex_10_data
        annex_10_data = json.load(file)
        print(annex_10_data)

    def test_percentage(self):
        """
        Checks whether more than a certain percentage of attributes can be found
        """
        # Loop through all annex files and corresponding years
        for annex_10_file, year in zip(annex_10_data, [2015, 2016, 2017, 2018, 2019, 2020, 2021]):
            # Get number of medicines of current annex 10 file
            found_attributes = len(annex_10_file[attr.assess_time_days_active])
            annex_path = f"{data_loc}/annex_10"
            filepath = ""
            # Get filepath of current annex 10 file (dictated by loop)
            for filename in os.listdir(annex_path):
                if str(year) in filename:
                    filepath = os.path.join(annex_path, filename)
            try:
                # Load Excel file
                excel_data = pd.read_excel(filepath)
            except FileNotFoundError:
                print("ANNEX 10 PARSER: File not found - " + filepath)
            # Clean the data
            excel_data = clean_df(excel_data)
            excel_data = excel_data[~excel_data["Active Time Elapsed"].isnull()]
            # Get one column to find amount of rows in Excel
            product_names = (excel_data["Product Name"].tolist())
            total_attributes = len(product_names)

            # Get the percentage of found attributes
            found_percentage = found_attributes/total_attributes * 100
            print(str(round(found_percentage, 2)) + '%')
            self.assertGreater(found_percentage, 79)

    def test_integer_results(self):
        for annex_10_file in annex_10_data:
            found_attributes = annex_10_file[attr.assess_time_days_active]
            for med in found_attributes:
                # Check if active time elapsed and clock stop elapsed are integers for all medicines and all annex files
                self.assertTrue(type(med[attr.active_time_elapsed]) == int)
                self.assertTrue(type(med[attr.assess_time_days_cstop]) == int)
