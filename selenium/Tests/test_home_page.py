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

  # check if the homepage contains 2 headings and that the headings are correct
  def test_headings(self):
    assert self.home_page.get_heading(0) == "Dashboard Tour"
    assert self.home_page.get_heading(1) == "Tools"
    
  # check whether the Start Tour button is rendered
  def test_tour(self):
    self.home_page.start_tour()
    assert self.home_page.get_heading(0) == "Dashboard Tour"

if __name__ == '__main__':
  unittest.main()
