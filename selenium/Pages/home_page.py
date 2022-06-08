# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from Pages.base_page import BasePage
from Pages.shared.search import Search
from Pages.shared.table import Table

class HomePage(BasePage, Search, Table):
  def __init__(self, driver):
    super().__init__(driver)
