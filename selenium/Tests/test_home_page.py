import sys
import os
import unittest

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.home_page import HomePage

class TestHomePage(WebDriverSetup):
  def setUp(self):
    super().setUp()
    self.home_page = HomePage(self.driver)
  
  # check if navigation bar opens and closes properly
  def test_navbar(self):
    assert self.home_page.navbar_is_closed() and not self.home_page.navbar_is_open()
    self.home_page.click_expand_collapse()
    assert self.home_page.navbar_is_open() and not self.home_page.navbar_is_closed()
    self.home_page.click_expand_collapse()
    assert self.home_page.navbar_is_closed() and not self.home_page.navbar_is_open()

  # check if the homepage contains 3 articles and that the links are correct
  def test_content(self):
    assert self.home_page.get_link(0) == "https://cbg-meb.nl/"
    assert self.home_page.get_link(1) == "https://www.ema.europa.eu/"
    assert self.home_page.get_link(2) == "https://ec.europa.eu/health/documents/community-register_en"
    
if __name__ == '__main__':
  unittest.main()
