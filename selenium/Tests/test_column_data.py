import sys
import os
import unittest
import random

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.data_page import DataPage
from Pages.search_page import SearchPage

class TestColumnData(WebDriverSetup):
  def setUp(self):
    super().setUp()
  
  # check if the column change propagates to all tables
  def test_column_data_change(self):
    data_page = DataPage(self.driver)
    select_row = random.randint(1, 25)
    data_page.select(select_row)
    column = random.randint(1, 5)
    data_page.change_column(0, column, "CoRapporteur")
    assert data_page.column_value(0, column) == "CoRapporteur"
    assert data_page.column_value(1, column) == "CoRapporteur"
    search_page = SearchPage(self.driver)
    assert search_page.column_value(0, column) == "CoRapporteur"

if __name__ == '__main__':
  unittest.main()
