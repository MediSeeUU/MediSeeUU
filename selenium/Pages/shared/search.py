# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from Resources.locators import SearchLocators

class Search():
  def search(self):
    table_buttons = self.driver.find_elements(*SearchLocators.BUTTON)
    table_buttons[0].click()

  def input_query(self, query):
    search_bar = self.driver.find_element(*SearchLocators.SEARCH_BAR)
    search_bar.send_keys(query)
  