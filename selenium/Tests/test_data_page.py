import sys
import os
import unittest
import random

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.data_page import DataPage
from Resources.locators import DataPageLocators

# test cases that are specifically located on the data page
class TestDataPage(WebDriverSetup):
  def setUp(self):
    super().setUp()
    # initialize the data page
    self.data_page = DataPage(self.driver)
  
  # test if the page is correct
  def test_data_url(self):
    assert self.data_page.current_url() == "http://localhost:3000/data"

  # test if checkboxes and actions on the right of the table remain visible
  def test_actions_visible(self):
    right_actions = self.driver.find_element(*DataPageLocators.RIGHT_ACTIONS)
    checkbox = self.driver.find_element(*DataPageLocators.SELECT)

    # first add a few columns to fill the space
    for _ in range(3):
      self.data_page.add_column(0)

    # any additional columns should not move the actions on the right further
    prev_x = right_actions.location["x"]
    for _ in range(5):
      self.data_page.add_column(0)

      x = right_actions.location["x"]
      assert x == prev_x, "actions moved to the right when adding a column"
      prev_x = x

    checkbox_x = checkbox.location["x"]
    self.driver.execute_script("document.querySelector('table').scrollBy(1000, 0);")
    assert checkbox.location['x'] == checkbox_x, "checkboxes moved to the left when scrolling"
  
  # check if the amount of results in main table changes
  def test_results_per_page(self):
    self.data_page.change_amount_of_results(100)
    assert self.data_page.amount_of_rows(0) == 100
  
  # select a few random rows in each of the first 10 pages and check if they are correctly put into the selected table
  def test_correct_selected(self):
    # deselect all datapoints
    self.data_page.select(0)
    # store all eu numbers of the selection
    eu_numbers = []
    # iterate over the first 10 pages
    for i in range(10):
      # determine random the amount of rows and which rows
      amount = random.randint(1, 5)
      ids = random.sample(range(1, self.data_page.default_rows), amount)
      # select the rows and store their eu number
      for id in ids:
        self.data_page.select(id)
        eu_numbers.append(self.data_page.table_value(0, id, 1))
      # navigate to the next page
      self.data_page.next_page(0)
    # keep a counter of the amount of rows of the second table
    count = 0
    # iterate over all the pages
    while self.data_page.current_page(1) <= self.data_page.last_page(1):
      # for each row check if it this point was selected before
      for i in range(self.data_page.amount_of_rows(1)):
        assert self.data_page.table_value(1, i + 1, 1) in eu_numbers
      # update the counter with the amount of rows of the page
      count += self.data_page.amount_of_rows(1)
      # navigate to the next page if possible, otherwise stop the loop
      if self.data_page.current_page(1) != self.data_page.last_page(1):
        self.data_page.next_page(1)
      else:
        break
    # check if the amount of selected points corresponds with the actual amount of selected points
    assert count == len(eu_numbers)
  
  # test if we navigate to the correct page
  def test_detailed_forward(self):
    # pick a random row
    id = random.randint(1, self.data_page.default_rows)
    # store the eu number of the row
    eu_number = self.data_page.table_value(0, id, 1)
    # click on the info icon in the table of the row
    self.data_page.open_detailed_info(0, id)
    # check if the url is correct
    assert self.data_page.current_url() == "http://localhost:3000/details/" + eu_number
  
  # test if data in the row changes when navigated to next page
  def test_next_page_new_rows(self):
    # store the eu numbers as identifiers of the rows
    eu_list = []
    # store all rows of the first page
    for i in range(self.data_page.default_rows):
      eu_list.append(self.data_page.table_value(0, i + 1, 1))
    # navigate to the next page
    self.data_page.next_page(0)
    # check if the new page is displayed correctly
    assert self.data_page.current_page(0) == "2"
    # check if all the eu numbers in this page are not in previous page
    for i in range(self.data_page.default_rows):
      assert self.data_page.table_value(0, i + 1, 1) not in eu_list
    # go back to the previous page and check if everything is exactly the same as before
    self.data_page.prev_page(0)
    assert self.data_page.current_page(0) == "1"
    for i in range(self.data_page.default_rows):
      assert self.data_page.table_value(0, i + 1, 1) == eu_list[i]
  
  # test if search, filter and sort are properly applied to the table
  def test_search_filter_sort(self):
    # search
    self.data_page.input_query("pfizer")
    self.data_page.search()
    # filter and sort
    self.data_page.open_menu()
    self.data_page.filter_select(1, "Short EU Number")
    self.data_page.filter_input(1, 1, "1300")
    self.data_page.sort_select(1, "Short EU Number")
    # need to do this twice to actually perform the select update
    self.data_page.sort_select(1, "Short EU Number")
    self.data_page.sort_order(1, "Descending")
    self.data_page.apply()
    # store the eu numbers (as they have been filtered and sorted)
    eu_numbers = []
    # iterate over the rows of the first page
    for i in range(self.data_page.amount_of_rows(0)):
      # store the eu number and check if it is properly filtered
      eu_number = int(self.data_page.table_value(0, i + 1, 1))
      assert eu_number >= 1300
      eu_numbers.append(int(eu_number))
    # check if the eu numbers are sorted properly
    assert all(eu_numbers[i] >= eu_numbers[i+1] for i in range(len(eu_numbers) - 1))
    columns = self.data_page.column_options()
    # iterate over the rows of the first page again
    for i in range(self.data_page.amount_of_rows(0)):
      inText = False
      # change column to change the data displayed in the table
      for column in columns:
        self.data_page.change_column(0, 1, column)
        # if the query is somewhere located in the text, the search has been applied properly on this row
        if ("pfizer" in self.data_page.table_value(0, i + 1, 1).lower()):
          inText = True
          break
      assert inText
  
  # check if the column change changes the data
  def test_column_change(self):
    # pick a random column and new value
    column = random.randint(1, self.data_page.amount_of_columns(0))
    current_column = self.data_page.column_value(0, column)
    columns = self.data_page.column_options()
    columns.remove(current_column)
    new_column_value = columns[random.randint(1, len(columns) - 1)]
    # store the data before the change
    data = []
    for i in range(self.data_page.amount_of_rows(0)):
      data.append(self.data_page.table_value(0, i + 1, column))
    # set the column to the new value and check if the data has changed
    self.data_page.change_column(0, column, new_column_value)
    for i in range(self.data_page.amount_of_rows(0)):
      new_value = self.data_page.table_value(0, i + 1, column)
      assert new_value not in data
    # check if the change has been applied everywhere
    assert self.data_page.column_value(0, column) == new_column_value
    assert self.data_page.column_value(1, column) == new_column_value
  
  # check if the column adds and removes are applied correctly and that the column is a new column
  def test_column_add_remove(self):
    # store the default columns
    columns = []
    for i in range(self.data_page.default_columns):
      columns.append(self.data_page.column_value(0, i + 1))
    # add a random amount of columns to the first table and make sure its value is an unseen one
    adds = random.randint(1, 5)
    for i in range(adds):
      self.data_page.add_column(0)
      column = self.data_page.column_value(0, self.data_page.default_columns + 1 + i)
      assert column not in columns
      columns.append(column)
    # check if the amount of columns in both tables are right
    assert self.data_page.amount_of_columns(0) == self.data_page.default_columns + adds
    assert self.data_page.amount_of_columns(1) == self.data_page.default_columns + adds
    # remove a random amount of columns (but lower than the add amount)
    removes = random.randint(1, adds)
    for i in range(removes):
      self.data_page.remove_column(0)
    # check if the amount of columns in both tables are right again
    assert self.data_page.amount_of_columns(0) == self.data_page.default_columns + adds - removes
    assert self.data_page.amount_of_columns(1) == self.data_page.default_columns + adds - removes
  
  # check if clear all clears the selected table
  def test_clear_all(self):
    # deselect all the datapoints in the table
    self.data_page.select(0)
    # the selected table must not be visible now
    assert not self.data_page.selected_visible()
    # select 8 random rows to select
    ids = random.sample(range(1, self.data_page.default_rows), 8)
    for id in ids:
      self.data_page.select(id)
    # the selected table must be visible now and amount of rows must be equal to 8
    assert self.data_page.selected_visible()
    assert self.data_page.amount_of_rows(1) == 8
    # check if the clear all button actually clears the table
    self.data_page.clear_all()
    assert not self.data_page.selected_visible()
  
  # check if a column sort actually sorts the data
  def test_sort_column(self):
    # press the sort button (first time should apply ascending order)
    self.data_page.sort_column(0, 1)
    # store all the column values
    data = []
    for i in range(self.data_page.amount_of_rows(0)):
      data.append(self.data_page.table_value(0, i + 1, 2).lower())
    # check if the data is ascendingly sorted
    assert all(data[i] <= data[i+1] for i in range(len(data) - 1))
    # press sort button again (second time should apply descending order)
    self.data_page.sort_column(0, 1)
    # store the column values again
    data = []
    for i in range(self.data_page.amount_of_rows(0)):
      data.append(self.data_page.table_value(0, i + 1, 2).lower())
    # check if the data is descendingly sorted
    assert all(data[i] >= data[i+1] for i in range(len(data) - 1))

if __name__ == '__main__':
  unittest.main()
