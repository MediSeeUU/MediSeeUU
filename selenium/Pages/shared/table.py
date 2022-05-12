from Resources.locators import TableLocators
from selenium.webdriver.support.ui import Select

class Table():
  def amount_of_rows(self, table):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    tbody = tables[table].find_element(*TableLocators.BODY)
    rows = tbody.find_elements(*TableLocators.ROW)
    return len(rows)
  
  def cell_value(self, table, row, column):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    row = tables[table].find_elements(*TableLocators.ROW)[row]
    key = row.find_elements(*TableLocators.CELL)[column]
    return key.text
  
  def table_value(self, table, row, column):
    if (table == 0):
      return self.cell_value(table, row, column)
    return self.cell_value(table, row, column - 1)
  
  def open_detailed_info(self, table, row):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    tbody = tables[table].find_element(*TableLocators.BODY)
    row = tbody.find_elements(*TableLocators.ROW)[row - 1]
    info = row.find_element(*TableLocators.INFO)
    info.click()
  
  def change_column(self, table, column, value):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    thead = tables[table].find_element(*TableLocators.HEAD)
    columns = thead.find_elements(*TableLocators.COLUMN)
    select = Select(columns[column - 1].find_element(*TableLocators.COLUMN_SELECT))
    select.select_by_visible_text(value)
  
  def column_value(self, table, column):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    thead = tables[table].find_element(*TableLocators.HEAD)
    columns = thead.find_elements(*TableLocators.COLUMN)
    select = Select(columns[column - 1].find_element(*TableLocators.COLUMN_SELECT))
    return select.first_selected_option.text
  
  def amount_of_columns(self, table):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    thead = tables[table].find_element(*TableLocators.HEAD)
    columns = thead.find_elements(*TableLocators.COLUMN)
    return len(columns)
  
  def add_column(self, table):
    add = self.driver.find_elements(*TableLocators.ADD_COLUMN)[table]
    add.click()
  
  def remove_column(self, table):
    remove = self.driver.find_elements(*TableLocators.REMOVE_COLUMN)[table]
    remove.click()
  
  def column_options(self):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    thead = tables[0].find_element(*TableLocators.HEAD)
    columns = thead.find_elements(*TableLocators.COLUMN)
    select = Select(columns[0].find_element(*TableLocators.COLUMN_SELECT))
    return list(map(lambda option: option.text, select.options))

