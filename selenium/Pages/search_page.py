from Pages.base_page import BasePage
from Pages.shared.table import Table
from Resources.locators import DataPageLocators

class SearchPage(BasePage, Table):
  def __init__(self, driver):
    super().__init__(driver)
    self.go_search()
