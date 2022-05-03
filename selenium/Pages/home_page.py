from Pages.base_page import BasePage
from Pages.shared.search import Search
from Resources.locators import HomePageLocators

class HomePage(BasePage, Search):
  def __init__(self, driver):
    super().__init__(driver)

    self.articles = self.driver.find_elements(*HomePageLocators.ARTICLE)
    self.links = self.driver.find_elements(*HomePageLocators.LINK)
  
  def get_link(self, id):
    return self.links[id].get_attribute('href')
