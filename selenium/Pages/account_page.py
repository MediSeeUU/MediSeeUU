from Pages.base_page import BasePage
from Resources.locators import AccountPageLocators

# account page containing the saved selections
class AccountPage(BasePage):
  def __init__(self, driver):
    super().__init__(driver)
    # navigate to account page
    self.go_account()
    
    # find all saved selections and store info
    selection_items = driver.find_elements(*AccountPageLocators.SAVED_SELECTION)
    self.saved_selections = dict()
    for selection in selection_items:
      name = selection.find_element(*AccountPageLocators.SAVED_NAME).text
      count = selection.find_element(*AccountPageLocators.SAVED_COUNT).text
      button = selection.find_element(*AccountPageLocators.SAVED_SELECT)
      value = { "count": count, "button": button }
      self.saved_selections[name] = value

  # checks if the given name occurs in the selection
  def name_in_selection(self, value):
    return value in self.saved_selections
  
  # returns the amount of selected points in the selection
  def selection_count(self, value):
    return int(self.saved_selections[value]["count"])
  
  # applies the selection
  def apply_selection(self, value):
    button = self.saved_selections[value]["button"]
    self.driver.execute_script("arguments[0].click();", button)
