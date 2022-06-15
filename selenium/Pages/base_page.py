from Resources.locators import BasePageLocators

# the base page contains functionality that is shared across all pages
class BasePage():
  def __init__(self, driver):
    # sets the driver locally
    self.driver = driver

    # locate the navigation bar and its items
    self.navbar = self.driver.find_element(*BasePageLocators.NAV)
    self.nav_items = self.driver.find_elements(*BasePageLocators.NAV_ITEM)
  
  # returns the current url of the driver
  def current_url(self):
    return self.driver.current_url
  
  # returns if the navbar is closed
  def navbar_is_closed(self):
    return "med-closed" in self.navbar.get_attribute('class')
  
  # returns if the navbar is open
  def navbar_is_open(self):
    return "med-open" in self.navbar.get_attribute('class')
  
  # expands and collapses the navbar
  def click_expand_collapse(self):
    self.nav_items[0].click()
  
  # navigates to home page
  def go_home(self):
    self.nav_items[1].click()

  # navigates to the info page
  def go_info(self):
    self.nav_items[2].click()
  
  # navigates to the data page
  def go_data(self):
    self.nav_items[3].click()
  
  # navigates to the visualization page
  def go_visualize(self):
    self.nav_items[4].click()
  
  def go_account(self):
    account = self.driver.find_element(*BasePageLocators.ACCOUNT_NAV)
    self.driver.execute_script("arguments[0].click();", account)
  
  # opens login pop-up and performs login action
  def login(self, username, password):
    login = self.driver.find_element(*BasePageLocators.LOGIN_NAV)
    login.click()
    inputs = self.driver.find_elements(*BasePageLocators.LOGIN_INPUT)
    inputs[0].send_keys(username)
    inputs[1].send_keys(password)
    button = self.driver.find_element(*BasePageLocators.LOGIN_BUTTON)
    button.click()
    self.driver.find_element(*BasePageLocators.ACCOUNT_NAV)
