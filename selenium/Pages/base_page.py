# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from Resources.locators import BasePageLocators

class BasePage():
  def __init__(self, driver):
    self.driver = driver

    self.navbar = self.driver.find_element(*BasePageLocators.NAV)
    self.nav_items = self.driver.find_elements(*BasePageLocators.NAV_ITEM)
  
  def current_url(self):
    return self.driver.current_url
  
  def navbar_is_closed(self):
    return "med-closed" in self.navbar.get_attribute('class')
  
  def navbar_is_open(self):
    return "med-open" in self.navbar.get_attribute('class')
  
  def click_expand_collapse(self):
    self.nav_items[0].click()
  
  def go_home(self):
    self.nav_items[1].click()

  def go_info(self):
    self.nav_items[2].click()
  
  def go_data(self):
    self.nav_items[3].click()
  
  def go_visualize(self):
    self.nav_items[4].click()
  