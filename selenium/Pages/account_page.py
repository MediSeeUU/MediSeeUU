# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from Pages.base_page import BasePage
from Resources.locators import AccountPageLocators

# account page containing the saved selections
class AccountPage(BasePage):
  def __init__(self, driver):
    super().__init__(driver)
    # navigate to account page
    self.go_account()
  
  def obtain_selections(self):
    # find all saved selections and store info in dictionary
    selection_items = self.driver.find_elements(*AccountPageLocators.SAVED_SELECTION)
    saved_selections = dict()
    for selection in selection_items:
      name = selection.find_element(*AccountPageLocators.SAVED_NAME).text
      count = selection.find_element(*AccountPageLocators.SAVED_COUNT).text
      select = selection.find_element(*AccountPageLocators.SAVED_SELECT)
      delete = selection.find_element(*AccountPageLocators.SAVED_DELETE)
      value = { "count": count, "select": select, "delete": delete }
      saved_selections[name] = value
    return saved_selections

  # checks if the given name occurs in the saved selections list
  def name_in_selection(self, value):
    return value in self.obtain_selections()
  
  # returns the amount of selected points in the selection
  def selection_count(self, value):
    saved_selections = self.obtain_selections()
    return int(saved_selections[value]["count"])
  
  # applies the selection
  def apply_selection(self, value):
    saved_selections = self.obtain_selections()
    button = saved_selections[value]["select"]
    self.driver.execute_script("arguments[0].click();", button)
  
  # removes the selection
  def delete_selection(self, value):
    saved_selections = self.obtain_selections()
    button = saved_selections[value]["delete"]
    self.driver.execute_script("arguments[0].click();", button)
