# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import sys
import os
import unittest

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.home_page import HomePage

# test cases that are specifically located on the home page
class TestHomePage(WebDriverSetup):
  def setUp(self):
    super().setUp()
    # initialize the home page
    self.home_page = HomePage(self.driver)

  # test if the page is correct
  def test_home_url(self):
    assert self.home_page.current_url() == "http://localhost:3000/"

  # check if navigation bar opens and closes properly
  def test_navbar(self):
    assert self.home_page.navbar_is_closed() and not self.home_page.navbar_is_open()
    self.home_page.click_expand_collapse()
    assert self.home_page.navbar_is_open() and not self.home_page.navbar_is_closed()
    self.home_page.click_expand_collapse()
    assert self.home_page.navbar_is_closed() and not self.home_page.navbar_is_open()

if __name__ == '__main__':
  unittest.main()
