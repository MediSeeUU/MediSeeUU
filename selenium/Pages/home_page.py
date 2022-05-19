from Pages.base_page import BasePage
from Pages.shared.search import Search
from Resources.locators import HomePageLocators

class HomePage(BasePage, Search):
  def __init__(self, driver):
    super().__init__(driver)
    self.go_home()

    self.headings = self.driver.find_elements(*HomePageLocators.HEADING)
  
  def get_heading(self, id):
    return self.headings[id].text

  def start_tour(self):
    start = self.driver.find_element(*HomePageLocators.TOUR)
    start.click()
