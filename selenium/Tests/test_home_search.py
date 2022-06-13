import sys
import os
import unittest

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.home_page import HomePage
from Pages.data_page import DataPage

class TestHomePage(WebDriverSetup):
  def setUp(self):
    super().setUp()
  
  # check if the search forwards properly
  def test_search_forward(self):
    home_page = HomePage(self.driver)
    home_page.input_query("100")
    home_page.search()
    data_page = DataPage(self.driver)
    columns = data_page.column_options()
    for i in range(data_page.amount_of_rows(0)):
      inText = False
      for column in columns:
        data_page.change_column(0, 1, column)
        if ("100" in data_page.table_value(0, i + 1, 1).lower()):
          inText = True
          break
      assert inText


if __name__ == '__main__':
  unittest.main()
