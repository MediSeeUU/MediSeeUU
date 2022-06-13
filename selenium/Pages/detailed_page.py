from Pages.base_page import BasePage
from Resources.locators import DetailedPageLocators

class DetailedPage(BasePage):
  def __init__(self, driver, id):
    super().__init__(driver)
    self.driver.get("http://localhost:3000/details/" + str(id))

    self.detailed_items = self.driver.find_elements(*DetailedPageLocators.DETAIL_ITEM)
    self.detailed_info = dict()
    for item in self.detailed_items:
      name = item.find_element(*DetailedPageLocators.DETAIL_NAME).text
      value = item.find_element(*DetailedPageLocators.DETAIL_VALUE).text
      self.detailed_info[name] = value
  
  def get_value(self, key):
    return self.detailed_info[key]
