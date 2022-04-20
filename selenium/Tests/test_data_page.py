import sys
import os
import unittest

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.data_page import DataPage

class TestDataPage(WebDriverSetup):
  def setUp(self):
    super().setUp()
    self.data_page = DataPage(self.driver)
  
  # test if the page is correctly navigated
  def test_correct_url(self):
    assert self.data_page.current_url() == "http://localhost:3000/data"
  
  # check if the amount of results in main table changes (by default 25)
  def test_results_per_page(self):
    assert self.data_page.amount_of_rows(0) == 25
    self.data_page.change_amount_of_results(50)
    assert self.data_page.amount_of_rows(0) == 50
  
  # check if pages change on command
  def test_page_changes(self):
    assert self.data_page.current_table_page(0) == "1"
    self.data_page.next_table_page(0)
    assert self.data_page.current_table_page(0) == "2"
    self.data_page.next_table_page(0)
    assert self.data_page.current_table_page(0) == "3"
    self.data_page.prev_table_page(0)
    assert self.data_page.current_table_page(0) == "2"
  
  # select 3 rows and see if there are 3 rows in the selected table
  def test_amount_of_selected(self):
    self.data_page.select(3)
    self.data_page.select(7)
    self.data_page.select(10)
    self.data_page.next_table_page(0)
    self.data_page.select(4)
    self.data_page.select(7)
    assert self.data_page.amount_of_rows(1) == 5
  
  # test if the correct row is selected
  def test_correct_selected(self):
    self.data_page.select(4)
    assert self.data_page.cell_value(1, 1, 0) == "4"
  
  # test if we navigate to the correct page
  def test_detailed_forward(self):
    self.data_page.open_detailed_info(0, 5)
    assert self.data_page.current_url() == "http://localhost:3000/details/6"

if __name__ == '__main__':
  unittest.main()
