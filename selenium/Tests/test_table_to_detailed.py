import sys
import os
import unittest
import random

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.data_page import DataPage
from Pages.detailed_page import DetailedPage

class TestTableToDetailed(WebDriverSetup):
  def setUp(self):
    super().setUp()
  
  # check if the content of the table is correct with the detailed info
  def test_detailed_info(self):
    data_page = DataPage(self.driver)
    data_page.select(0)
    data_page.change_amount_of_results(300)
    id = random.randint(1, 300)
    data = dict()
    for i in range(data_page.default_columns):
      name = data_page.column_value(0, i + 1)
      value = data_page.table_value(0, id, i + 1)
      data[name] = value
    detailed_page = DetailedPage(self.driver, data['Short EU Number'])
    for key in data:
      assert data[key] == detailed_page.get_value(key)


if __name__ == '__main__':
  unittest.main()
