from Pages.base_page import BasePage
from Resources.locators import HomePageLocators

class HomePage(BasePage):
  def __init__(self, driver):
    super().__init__(driver)

    self.articles = self.driver.find_elements(*HomePageLocators.ARTICLE)
    self.links = self.driver.find_elements(*HomePageLocators.LINK)
  
  def amount_of_articles(self):
    return len(self.articles)
  
  def get_link(self, id):
    return self.links[id].get_attribute('href')
