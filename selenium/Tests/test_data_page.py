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
  def test_data_url(self):
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
  
  # select 3 random rows in each of the first 10 pages and check if they are correctly put into the select table
  def test_correct_selected(self):
    eu_numbers = []
    for i in range(10):
      ids = random.sample(range(1, 25), 3)
      for id in ids:
        self.data_page.select(id)
        eu_numbers.append(self.data_page.table_value(0, id, 1))
      self.data_page.next_table_page(0)
    assert self.data_page.amount_of_rows(1) == 25
    for i in range(24):
      assert self.data_page.table_value(1, i + 1, 1) in eu_numbers
    self.data_page.next_table_page(1)
    assert self.data_page.amount_of_rows(1) == 5
    for i in range(4):
      assert self.data_page.table_value(1, i + 1, 1) in eu_numbers
  
  # test if we navigate to the correct page
  def test_detailed_forward(self):
    id = random.randint(1, 25)
    first_value = self.data_page.table_value(0, id, 1)
    self.data_page.open_detailed_info(0, id)
    assert self.data_page.current_url() == "http://localhost:3000/details/" + first_value
  
  # test if data in the row changes when navigated to next page
  def test_next_page_new_rows(self):
    eu_list = []
    for i in range(24):
      eu_list.append(self.data_page.table_value(0, i + 1, 1))
    self.data_page.next_table_page(0)
    for i in range(24):
      assert self.data_page.table_value(0, i + 1, 1) not in eu_list
  
  # test if filter and sort are properly applied to the table
  def test_filter_and_sort(self):
    self.data_page.open_menu()
    self.data_page.sort_select(1, "EUNoShort")
    self.data_page.sort_order(1, "Descending")
    self.data_page.filter_select(1, "EUNoShort")
    self.data_page.filter_input(1, 1, "10")
    self.data_page.add_filter()
    self.data_page.filter_select(2, "Rapporteur")
    self.data_page.filter_input(2, 1, "United Kingdom")
    self.data_page.apply()
    self.data_page.change_column(2, "Rapporteur")
    eu_numbers = []
    for i in range(self.data_page.amount_of_rows(0) - 1):
      eu_number = self.data_page.table_value(0, i + 1, 1)
      assert "10" in eu_number
      assert "United Kingdom" in self.data_page.table_value(0, i + 1, 2)
      eu_numbers.append(int(eu_number))
    assert all(eu_numbers[i] >= eu_numbers[i+1] for i in range(len(eu_numbers) - 1))

if __name__ == '__main__':
  unittest.main()
