import sys
import os
import unittest
import random

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.search_page import SearchPage

class TestSearchPage(WebDriverSetup):
  def setUp(self):
    super().setUp()
    self.search_page = SearchPage(self.driver)
  
  # test if the page is correct
  def test_search_url(self):
    assert self.search_page.current_url() == "http://localhost:3000/search"

if __name__ == '__main__':
  unittest.main()
