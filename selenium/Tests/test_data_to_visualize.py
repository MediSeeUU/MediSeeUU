import sys
import os
import unittest
import random
import time

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.data_page import DataPage
from Pages.visualize_page import VisualizePage

class TestDataToVisualize(WebDriverSetup):
  def setUp(self):
    super().setUp()
  
  # check if the right countries are listed in the visualize page
  def test_categories(self):
    data_page = DataPage(self.driver)
    data_page.change_amount_of_results(300)
    data_page.change_column(1, "Rapporteur")
    countries = []
    ids = random.sample(range(1, 300), 10)
    for i in ids:
      data_page.select(i)
      countries.append(data_page.first_value(0, i))
    visualize_page = VisualizePage(self.driver)
    cat_list = visualize_page.possible_categories()
    for cat in cat_list:
      assert cat in countries

if __name__ == '__main__':
  unittest.main()
