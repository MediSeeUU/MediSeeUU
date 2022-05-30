from Pages.base_page import BasePage
from Pages.shared.search import Search
from Pages.shared.table import Table

class HomePage(BasePage, Search, Table):
  def __init__(self, driver):
    super().__init__(driver)
