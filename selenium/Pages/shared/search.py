from Resources.locators import SearchLocators

# search component on the site which is used by the home and data page
class Search():
  # press search button
  def search(self):
    table_buttons = self.driver.find_elements(*SearchLocators.BUTTON)
    self.driver.execute_script("arguments[0].click();", table_buttons[0])

  # change input query
  def input_query(self, query):
    search_bar = self.driver.find_element(*SearchLocators.SEARCH_BAR)
    search_bar.send_keys(query)
