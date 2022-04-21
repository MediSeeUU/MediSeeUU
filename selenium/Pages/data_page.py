from Pages.base_page import BasePage
from Pages.shared.table import Table
from Resources.locators import DataPageLocators
from selenium.webdriver.support.ui import Select

class DataPage(BasePage, Table):
  def __init__(self, driver):
    super().__init__(driver)
    self.go_data()
  
  def current_table_page(self, table):
    return self.driver.find_elements(*DataPageLocators.SELECTED_PAGE)[table].text
  
  def next_table_page(self, table):
    next_page = self.driver.find_elements(*DataPageLocators.NEXT_PAGE)[table]
    self.driver.execute_script("arguments[0].click();", next_page)
  
  def prev_table_page(self, table):
    prev_page = self.driver.find_elements(*DataPageLocators.PREV_PAGE)[table]
    self.driver.execute_script("arguments[0].click();", prev_page)
  
  def select_all(self):
    selects = self.driver.find_elements(*DataPageLocators.SELECT)
    selects[0].click()
  
  def select(self, id):
    selects = self.driver.find_elements(*DataPageLocators.SELECT)
    self.driver.execute_script("arguments[0].click();", selects[id])
  
  def change_amount_of_results(self, value):
    self.results = self.driver.find_element(*DataPageLocators.RESULTS_PER_PAGE)
    self.results.send_keys(value)
  
  def open_menu(self):
    self.table_buttons = self.driver.find_elements(*DataPageLocators.BUTTON)
    self.table_buttons[0].click()
  
  def add_filter(self):
    add = self.driver.find_element(*DataPageLocators.MenuLocators.ADD_FILTER)
    add.click()
  
  def filter_select(self, id, value):
    filter_item = self.driver.find_elements(*DataPageLocators.MenuLocators.FILTER_ITEM)[id - 1]
    select = Select(filter_item.find_element(*DataPageLocators.MenuLocators.SELECT))
    select.select_by_visible_text(value)
  
  def filter_input(self, id, bid, value):
    filter_item = self.driver.find_elements(*DataPageLocators.MenuLocators.FILTER_ITEM)[id - 1]
    input_item = filter_item.find_elements(*DataPageLocators.MenuLocators.INPUT)[bid - 1]
    input_item.send_keys(value)
  
  def sort_select(self, id, value):
    sort_item = self.driver.find_elements(*DataPageLocators.MenuLocators.SORT_ITEM)[id - 1]
    select = Select(sort_item.find_elements(*DataPageLocators.MenuLocators.SELECT)[0])
    select.select_by_visible_text(value)
  
  def sort_order(self, id, value):
    sort_item = self.driver.find_elements(*DataPageLocators.MenuLocators.SORT_ITEM)[id - 1]
    select = Select(sort_item.find_elements(*DataPageLocators.MenuLocators.SELECT)[1])
    select.select_by_visible_text(value)
  
  def apply(self):
    apply = self.driver.find_element(*DataPageLocators.MenuLocators.APPLY)
    apply.click()
