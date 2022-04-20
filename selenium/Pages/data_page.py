from Pages.base_page import BasePage
from Resources.locators import DataPageLocators

class DataPage(BasePage):
  def __init__(self, driver):
    super().__init__(driver)
    self.go_data()

    self.table_buttons = self.driver.find_elements(*DataPageLocators.BUTTON)
    self.selects = self.driver.find_elements(*DataPageLocators.SELECT)
    self.results = self.driver.find_element(*DataPageLocators.RESULTS_PER_PAGE)
  
  def open_menu(self):
    self.table_buttons[0].click()
  
  def select_all(self):
    self.selects[0].click()
  
  def select(self, id):
    self.selects[id].click()
  
  def amount_of_rows(self, id):
    tables = self.driver.find_elements(*DataPageLocators.TABLE)
    tbody = tables[id].find_element(*DataPageLocators.BODY)
    rows = tbody.find_elements(*DataPageLocators.ROW)
    return len(rows)
  
  def change_amount_of_results(self, value):
    self.results.send_keys(value)
  
  def cell_value(self, table, row, column):
    tables = self.driver.find_elements(*DataPageLocators.TABLE)
    tbody = tables[table].find_element(*DataPageLocators.BODY)
    row = tbody.find_elements(*DataPageLocators.ROW)[row]
    key = row.find_elements(*DataPageLocators.CELL)[column]
    return key.text
