from Pages.base_page import BasePage
from Pages.shared.search import Search
from Resources.locators import InfoPageLocators

class InfoPage(BasePage, Search):
  def __init__(self, driver):
    super().__init__(driver)

    self.articles = self.driver.find_elements(*InfoPageLocators.ARTICLE)
    self.links = self.driver.find_elements(*InfoPageLocators.LINK)
  
  def get_link(self, id):
    return self.links[id].get_attribute('href')
