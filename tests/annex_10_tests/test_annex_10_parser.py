from unittest import TestCase
from scraping.file_parser.annex_10_parser import __main__ as annex_10_parser
import json
import os
import pandas as pd

data_loc = "../../data"
annex_10_data = {}


def clean_df(excel_data: pd.DataFrame) -> pd.DataFrame:
    """
    Args:
        excel_data (pd.DataFrame): the contents of the Excel file

    Returns:
        pd.DataFrame: the cleaned contents of the Excel file
    """
    # Clean null lines
    excel_data = excel_data[~excel_data["Unnamed: 0"].isnull()]
    # Remove all before "Product Name"
    x = excel_data.index[excel_data["Unnamed: 0"] == "Product Name"].tolist()[0]
    excel_data = excel_data.truncate(before=x).reset_index()
    # Set index to first row
    excel_data.columns = excel_data.iloc[0]
    excel_data = excel_data.truncate(before=1).reset_index()
    # Remove redundant columns
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
        file = open("annex_10_parser.json", "r")
        global annex_10_data
        annex_10_data = json.load(file)

    def test_annex_10(self):
        """
        Checks whether more than a certain percentage of attributes can be found
        """
        for annex_10_file, year in zip(annex_10_data, [2015, 2016, 2017, 2018, 2019, 2020, 2021]):
            found_attributes = len(annex_10_file['active_clock_elapseds'])
            annex_path = "../../data/annex_10"
            filepath = ""
            for filename in os.listdir(annex_path):
                if str(year) in filename:
                    filepath = os.path.join(annex_path, filename)
            try:
                excel_data = pd.read_excel(filepath)
            except FileNotFoundError:
                log.warning("ANNEX 10 PARSER: File not found - " + filepath)
                return annex10s
            excel_data = clean_df(excel_data)
            excel_data = excel_data[~excel_data["Active Time Elapsed"].isnull()]
            # Get all relevant data from columns
            product_names = (excel_data["Product Name"].tolist())
            total_attributes = len(product_names)

            # Get the percentage of found attributes
            found_percentage = found_attributes/total_attributes * 100
            print(str(round(found_percentage, 2)) + '%')
            self.assertGreater(found_percentage, 79)