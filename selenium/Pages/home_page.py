from Pages.base_page import BasePage
from Pages.shared.search import Search

class HomePage(BasePage, Search):
  def __init__(self, driver):
    super().__init__(driver)
