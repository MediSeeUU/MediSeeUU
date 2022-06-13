import sys
import os
import unittest
import random

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.data_page import DataPage
from Pages.detailed_page import DetailedPage

# test cases for data to detailed info page
class TestDataToDetailed(WebDriverSetup):
  def setUp(self):
    super().setUp()
  
  # check if the content of the table is correct with the detailed info
  def test_detailed_info(self):
    # intialize the data page
    data_page = DataPage(self.driver)
    # deselect all datapoints and select a random row out of 300 rows
    data_page.select(0)
    data_page.change_amount_of_results(300)
    id = random.randint(1, 300)
    # store the info in the table in a dictionary
    data = dict()
    for i in range(data_page.default_columns):
      name = data_page.column_value(0, i + 1)
      value = data_page.table_value(0, id, i + 1)
      data[name] = value
    # go to the appropriate detailed page
    detailed_page = DetailedPage(self.driver, data['Short EU Number'])
    # check if each stored info in the table corresponds with the info displayed on the detailed info page
    for key in data:
      assert data[key] == detailed_page.get_value(key)


if __name__ == '__main__':
  unittest.main()
