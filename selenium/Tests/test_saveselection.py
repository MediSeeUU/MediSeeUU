# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import sys
import os
import unittest
import random
import string

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.base_page import BasePage
from Pages.data_page import DataPage
from Pages.account_page import AccountPage

# generates a random string of specified length
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

# test cases for data to detailed info page
class TestSaveSelection(WebDriverSetup):
  def setUp(self):
    super().setUp()
  
  # test if a selection is saved and can be loaded in and removed again
  def test_saveselection(self):
    # navigate to data page and login
    data_page = DataPage(self.driver)
    # perform login action
    base_page = BasePage(self.driver)
    base_page.login("selenium", "fullcoverage")
    # deselect all datapoints
    data_page.select(0)
    # store all eu numbers of the selection
    eu_numbers = []
    # iterate over the first 10 pages
    count = 0
    for i in range(10):
      # determine random the amount of rows and which rows
      amount = random.randint(1, 5)
      ids = random.sample(range(1, data_page.default_rows), amount)
      # select the rows and store their eu number
      for id in ids:
        data_page.select(id)
        eu_numbers.append(data_page.table_value(0, id, 1))
      count += amount
      # navigate to the next page
      data_page.next_page(0)
    # save selection with a random name of length 10
    data_page.open_save_menu()
    name = randomword(10)
    data_page.save_input(name)
    data_page.save()
    # reset the selection
    data_page.select(0)
    # navigate to account page
    account_page = AccountPage(self.driver)
    # check if the basic descriptions are correct
    assert account_page.name_in_selection(name)
    assert account_page.selection_count(name) == count
    # apply selection and go back to the data page
    account_page.apply_selection(name)
    account_page.go_data()
    # iterate over all the pages in the selected table
    count_select = 0
    while data_page.current_page(1) <= data_page.last_page(1):
      # for each row check if it this point was selected before
      for i in range(data_page.amount_of_rows(1)):
        assert data_page.table_value(1, i + 1, 1) in eu_numbers
      # update the counter with the amount of rows of the page
      count_select += data_page.amount_of_rows(1)
      # navigate to the next page if possible, otherwise stop the loop
      if data_page.current_page(1) != data_page.last_page(1):
        data_page.next_page(1)
      else:
        break
    # check if the counts are correct again
    assert count == count_select
    # go back to the account page and delete the selection
    data_page.go_account()
    account_page.delete_selection(name)
    account_page.go_data()
    data_page.go_account()
    # finally check if the selection is removed again
    assert not account_page.name_in_selection(name)

if __name__ == '__main__':
  unittest.main()
