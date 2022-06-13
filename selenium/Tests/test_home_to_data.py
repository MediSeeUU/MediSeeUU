import sys
import os
import unittest

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.home_page import HomePage
from Pages.data_page import DataPage

# test cases for home to data page
class TestHomeToData(WebDriverSetup):
  def setUp(self):
    super().setUp()
  
  # check if the search forwards properly and is applied correctly
  def test_search_forward(self):
    # navigate to home page and do a search action
    home_page = HomePage(self.driver)
    home_page.input_query("100")
    home_page.search()
    assert home_page.current_url() == "http://localhost:3000/data"
    # initialize data page
    data_page = DataPage(self.driver)
    columns = data_page.column_options()
    # iterate over the rows of the first page
    for i in range(data_page.amount_of_rows(0)):
      inText = False
      # iterate over all the columns
      for column in columns:
        # if the query is in the text value, then the search is applied correctly to this row
        data_page.change_column(0, 1, column)
        if ("100" in data_page.table_value(0, i + 1, 1).lower()):
          inText = True
          break
      assert inText

if __name__ == '__main__':
  unittest.main()
