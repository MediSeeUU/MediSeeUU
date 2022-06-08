from Resources.locators import SearchLocators

class Search():
  def search(self):
    table_buttons = self.driver.find_elements(*SearchLocators.BUTTON)
    table_buttons[0].click()

  def input_query(self, query):
    search_bar = self.driver.find_element(*SearchLocators.SEARCH_BAR)
    search_bar.send_keys(query)
  