from Pages.base_page import BasePage
from Pages.shared.search import Search

# home page containing the search component
class HomePage(BasePage, Search):
  def __init__(self, driver):
    super().__init__(driver)
