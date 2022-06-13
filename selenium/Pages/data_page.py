from Pages.base_page import BasePage
from Pages.shared.table import Table
from Pages.shared.search import Search
from Resources.locators import DataPageLocators, TableLocators
from selenium.webdriver.support.ui import Select

# data page with the tables and search components
class DataPage(BasePage, Table, Search):
  def __init__(self, driver):
    super().__init__(driver)
    # navigate to data page
    self.go_data()

    # store the initial amount of rows and columns (of the first table)
    self.default_rows = self.amount_of_rows(0)
    self.default_columns = self.amount_of_columns(0)
  
  # changes the amount of results in the table
  def change_amount_of_results(self, value):
    results = self.driver.find_element(*DataPageLocators.RESULTS_PER_PAGE)
    results.send_keys(value)
  
  # opens the sort and filter menu
  def open_menu(self):
    table_buttons = self.driver.find_elements(*DataPageLocators.BUTTON)
    self.driver.execute_script("arguments[0].click();", table_buttons[1])
  
  # adds a filter item in the menu
  def add_filter(self):
    add = self.driver.find_element(*DataPageLocators.MenuLocators.ADD_FILTER)
    self.driver.execute_script("arguments[0].click();", add)
  
  # changes the selected option in the filter item
  def filter_select(self, id, value):
    filter_item = self.driver.find_elements(*DataPageLocators.MenuLocators.FILTER_ITEM)[id - 1]
    select = Select(filter_item.find_element(*DataPageLocators.MenuLocators.SELECT))
    select.select_by_visible_text(value)
  
  # changes the input in the filter item
  def filter_input(self, id, bid, value):
    filter_item = self.driver.find_elements(*DataPageLocators.MenuLocators.FILTER_ITEM)[id - 1]
    input_item = filter_item.find_elements(*DataPageLocators.MenuLocators.INPUT)[bid - 1]
    input_item.send_keys(value)
  
  # changes the selected option in the sort item
  def sort_select(self, id, value):
    sort_item = self.driver.find_elements(*DataPageLocators.MenuLocators.SORT_ITEM)[id - 1]
    select = Select(sort_item.find_elements(*DataPageLocators.MenuLocators.SELECT)[0])
    select.select_by_visible_text(value)
  
  # changes the sorting order in the sort item
  def sort_order(self, id, value):
    sort_item = self.driver.find_elements(*DataPageLocators.MenuLocators.SORT_ITEM)[id - 1]
    select = Select(sort_item.find_elements(*DataPageLocators.MenuLocators.SELECT)[1])
    select.select_by_visible_text(value)
  
  # applies the filters and sorters from the menu
  def apply(self):
    apply = self.driver.find_element(*DataPageLocators.MenuLocators.APPLY)
    self.driver.execute_script("arguments[0].click();", apply)
  
  # clears all datapoints in the selected table
  def clear_all(self):
    clear_all = self.driver.find_element(*DataPageLocators.CLEAR_ALL)
    self.driver.execute_script("arguments[0].click();", clear_all)
  
  # selects a datapoint in the first table
  def select(self, id):
    selects = self.driver.find_elements(*DataPageLocators.SELECT)
    self.driver.execute_script("arguments[0].click();", selects[id])
  
  # checks if the selected table is visible (or if there are datapoints selected)
  def selected_visible(self):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    return len(tables) > 1
  
  # returns the current table page
  def current_page(self, table):
    return self.driver.find_elements(*DataPageLocators.SELECTED_PAGE)[table].text
  
  # returns the last table page
  def last_page(self, table):
    bottom_holder = self.driver.find_elements(*DataPageLocators.BOTTOM_HOLDER)[table]
    return bottom_holder.find_elements(*DataPageLocators.PAGES)[-1].text
  
  # navigates to the next table page
  def next_page(self, table):
    next_page = self.driver.find_elements(*DataPageLocators.NEXT_PAGE)[table]
    self.driver.execute_script("arguments[0].click();", next_page)
  
  # navigates to the previous table page
  def prev_page(self, table):
    prev_page = self.driver.find_elements(*DataPageLocators.PREV_PAGE)[table]
    self.driver.execute_script("arguments[0].click();", prev_page)
