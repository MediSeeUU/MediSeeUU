# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from Pages.base_page import BasePage
from Resources.locators import InfoPageLocators

class InfoPage(BasePage):
  def __init__(self, driver):
    super().__init__(driver)
    self.go_info()

    self.links = self.driver.find_elements(*InfoPageLocators.LINK)
  
  def get_link(self, id):
    return self.links[id].get_attribute('href')
