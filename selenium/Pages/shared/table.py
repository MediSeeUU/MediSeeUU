from Resources.locators import TableLocators
from selenium.webdriver.support.ui import Select

# table component on the site which is used by the data and visualization page
class Table():
  # returns the amount of rows of the specified table
  def amount_of_rows(self, table):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    tbody = tables[table].find_element(*TableLocators.BODY)
    rows = tbody.find_elements(*TableLocators.ROW)
    return len(rows)
  
  # returns the value of the specified cell in the table
  def cell_value(self, table, row, column):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    row = tables[table].find_elements(*TableLocators.ROW)[row]
    key = row.find_elements(*TableLocators.CELL)[column]
    return key.text
  
  # generic function that returns in the specified table the cell value
  def table_value(self, table, row, column):
    if (table == 0):
      return self.cell_value(table, row, column)
    return self.cell_value(table, row, column - 1)
  
  # clicks on the detailed info of the row in the table
  def open_detailed_info(self, table, row):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    tbody = tables[table].find_element(*TableLocators.BODY)
    row = tbody.find_elements(*TableLocators.ROW)[row - 1]
    info = row.find_element(*TableLocators.INFO)
    self.driver.execute_script("arguments[0].click();", info)
  
  # changes the column to the different variable value
  def change_column(self, table, column, value):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    thead = tables[table].find_element(*TableLocators.HEAD)
    columns = thead.find_elements(*TableLocators.COLUMN)
    select = Select(columns[column - 1].find_element(*TableLocators.COLUMN_SELECT))
    select.select_by_visible_text(value)
  
  # returns the variable value in the column
  def column_value(self, table, column):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    thead = tables[table].find_element(*TableLocators.HEAD)
    columns = thead.find_elements(*TableLocators.COLUMN)
    select = Select(columns[column - 1].find_element(*TableLocators.COLUMN_SELECT))
    return select.first_selected_option.text
  
  # returns the amount of columns in the table
  def amount_of_columns(self, table):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    thead = tables[table].find_element(*TableLocators.HEAD)
    columns = thead.find_elements(*TableLocators.COLUMN)
    return len(columns)
  
  # adds a column at the end of the table
  def add_column(self, table):
    add = self.driver.find_elements(*TableLocators.ADD_COLUMN)[table]
    self.driver.execute_script("arguments[0].click();", add)
  
  # removes the last column from the table
  def remove_column(self, table):
    remove = self.driver.find_elements(*TableLocators.REMOVE_COLUMN)[table]
    self.driver.execute_script("arguments[0].click();", remove)
  
  # returns a list of variables that can be chosen in the columns
  def column_options(self):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    thead = tables[0].find_element(*TableLocators.HEAD)
    columns = thead.find_elements(*TableLocators.COLUMN)
    select = Select(columns[0].find_element(*TableLocators.COLUMN_SELECT))
    return list(map(lambda option: option.text, select.options))

  # clicks on the sort button of the column in the table
  def sort_column(self, table, column):
    tables = self.driver.find_elements(*TableLocators.TABLE)
    sort = tables[table].find_elements(*TableLocators.SORT_COLUMN)[column]
    self.driver.execute_script("arguments[0].click();", sort)
