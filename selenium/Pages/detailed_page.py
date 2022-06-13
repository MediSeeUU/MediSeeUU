from Pages.base_page import BasePage
from Resources.locators import DetailedPageLocators

# detailed info page of a single medicine
class DetailedPage(BasePage):
  def __init__(self, driver, id):
    super().__init__(driver)
    # navigate to the detailed info page of medicine with the given eu number
    driver.get("http://localhost:3000/details/" + str(id))

    # store the detailed info displayed on the page
    detailed_items = driver.find_elements(*DetailedPageLocators.DETAIL_ITEM)
    self.detailed_info = dict()
    for item in self.detailed_items:
      name = item.find_element(*DetailedPageLocators.DETAIL_NAME).text
      value = item.find_element(*DetailedPageLocators.DETAIL_VALUE).text
      self.detailed_info[name] = value
  
  # returns the value of the given variable
  def get_value(self, key):
    return self.detailed_info[key]
