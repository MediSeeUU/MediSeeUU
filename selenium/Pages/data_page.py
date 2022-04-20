from Pages.base_page import BasePage
from Resources.locators import DataPageLocators

class DataPage(BasePage):
  def __init__(self, driver):
    super().__init__(driver)
    self.go_data()
  
  def open_menu(self):
    self.table_buttons = self.driver.find_elements(*DataPageLocators.BUTTON)
    self.table_buttons[0].click()
  
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
  
  def amount_of_rows(self, id):
    tables = self.driver.find_elements(*DataPageLocators.TABLE)
    tbody = tables[id].find_element(*DataPageLocators.BODY)
    rows = tbody.find_elements(*DataPageLocators.ROW)
    return len(rows)
  
  def change_amount_of_results(self, value):
    self.results = self.driver.find_element(*DataPageLocators.RESULTS_PER_PAGE)
    self.results.send_keys(value)
  
  def cell_value(self, table, row, column):
    tables = self.driver.find_elements(*DataPageLocators.TABLE)
    row = tables[table].find_elements(*DataPageLocators.ROW)[row]
    key = row.find_elements(*DataPageLocators.CELL)[column]
    return key.text
  
  def first_value(self, table, id):
    if (table == 0):
      return self.cell_value(table, id, 1)
    return self.cell_value(table, id, 0)
  
  def open_detailed_info(self, table, id):
    tables = self.driver.find_elements(*DataPageLocators.TABLE)
    tbody = tables[table].find_element(*DataPageLocators.BODY)
    row = tbody.find_elements(*DataPageLocators.ROW)[id - 1]
    info = row.find_element(*DataPageLocators.INFO)
    info.click()
  
  def change_column(self, id, value):
    table = self.driver.find_elements(*DataPageLocators.TABLE)[0]
    thead = table.find_element(*DataPageLocators.HEAD)
    columns = thead.find_elements(*DataPageLocators.COLUMN)
    select = columns[id - 1].find_element(*DataPageLocators.COLUMN_SELECT)
    select.send_keys(value)
