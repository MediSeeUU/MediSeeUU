import sys
import os
import unittest
import random

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
  
  # select 8 rows and see if there are 8 rows in the selected table
  def test_amount_of_selected(self):
    self.data_page.select(7)
    self.data_page.select(13)
    self.data_page.next_table_page(0)
    self.data_page.select(11)
    self.data_page.select(7)
    self.data_page.next_table_page(0)
    self.data_page.select(20)
    self.data_page.select(16)
    self.data_page.next_table_page(0)
    self.data_page.select(11)
    self.data_page.select(19)
    assert self.data_page.amount_of_rows(1) == 8
  
  # test if the correct row is selected
  def test_correct_selected(self):
    id = random.randint(1, 25)
    self.data_page.select(id)
    assert self.data_page.eu_number(0, id) == self.data_page.eu_number(1, 1)
  
  # test if we navigate to the correct page
  def test_detailed_forward(self):
    id = random.randint(1, 25)
    eu_number = self.data_page.eu_number(0, id)
    self.data_page.open_detailed_info(0, id)
    assert self.data_page.current_url() == "http://localhost:3000/details/" + eu_number
  
  # test if data in the row changes when navigated to next page
  def test_next_page_new_rows(self):
    eu_list = []
    for i in range(24):
      eu_list.append(self.data_page.eu_number(0, i + 1))
    self.data_page.next_table_page(0)
    for i in range(24):
      assert self.data_page.eu_number(0, i + 1) not in eu_list

if __name__ == '__main__':
  unittest.main()
