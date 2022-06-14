import sys
import os
import unittest
import random

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.data_page import DataPage
from Pages.visualize_page import VisualizePage

# test cases for data to visualization page
class TestDataToVisualize(WebDriverSetup):
  def setUp(self):
    super().setUp()
  
  # check if the right countries are listed in the visualize page
  def test_categories(self):
    # navigate to data page
    data_page = DataPage(self.driver)
    # deselect all selected datapoints and display the first 300 rows
    data_page.select(0)
    data_page.change_amount_of_results(300)
    # set the columns to the values we want to store
    years = []
    data_page.change_column(0, 1, "Decision Year")
    countries = []
    data_page.change_column(0, 2, "Rapporteur")
    # select a few random datapoints and store its values
    ids = random.sample(range(1, 300), random.randint(5, 15))
    for i in ids:
      data_page.select(i)
      years.append(data_page.table_value(0, i, 1))
      countries.append(data_page.table_value(0, i, 2))
    # navigate to visualization page
    visualize_page = VisualizePage(self.driver)
    cat_list_xaxis = visualize_page.possible_categories(0)
    cat_list_yaxis = visualize_page.possible_categories(1)
    # check if the categories are displayed as expected
    for cat in cat_list_xaxis:
      assert cat in years
    for cat in cat_list_yaxis:
      assert cat in countries

if __name__ == '__main__':
  unittest.main()
