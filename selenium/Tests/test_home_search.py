import sys
import os
import unittest

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.home_page import HomePage
from Pages.data_page import DataPage

class TestHomeSearch(WebDriverSetup):
  def setUp(self):
    super().setUp()
    self.home_page = HomePage(self.driver)

    # check if navigation bar opens and closes properly
  def test_navbar(self):
    assert self.home_page.navbar_is_closed() and not self.home_page.navbar_is_open()
    self.home_page.click_expand_collapse()
    assert self.home_page.navbar_is_open() and not self.home_page.navbar_is_closed()
    self.home_page.click_expand_collapse()
    assert self.home_page.navbar_is_closed() and not self.home_page.navbar_is_open()
  
  # check if the search forwards properly
  def test_search_forward(self):
    self.home_page.input_query("100")
    self.home_page.search()
    columns = self.home_page.column_options()
    for i in range(self.home_page.amount_of_rows(0)):
      inText = False
      for column in columns:
        self.home_page.change_column(0, 1, column)
        if ("100" in self.home_page.table_value(0, i + 1, 1).lower()):
          inText = True
          break
      assert inText
      
if __name__ == '__main__':
  unittest.main()
