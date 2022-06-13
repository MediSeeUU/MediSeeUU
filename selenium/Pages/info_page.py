from Pages.base_page import BasePage
from Resources.locators import InfoPageLocators

# info page containing information about the site
class InfoPage(BasePage):
  def __init__(self, driver):
    super().__init__(driver)
    # navigate to the info page
    self.go_info()

    # find all links on the site
    self.links = self.driver.find_elements(*InfoPageLocators.LINK)
  
  # get the specified link
  def get_link(self, id):
    return self.links[id].get_attribute('href')
