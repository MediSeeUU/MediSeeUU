import sys
import os
import unittest

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.info_page import InfoPage

class TestInfoPage(WebDriverSetup):
  def setUp(self):
    super().setUp()
    self.info_page = InfoPage(self.driver)

  # check if the infopage contains 3 articles and that the links are correct
  def test_content(self):
    assert self.info_page.get_link(0) == "https://cbg-meb.nl/"
    assert self.info_page.get_link(1) == "https://www.ema.europa.eu/"
    assert self.info_page.get_link(2) == "https://ec.europa.eu/health/documents/community-register_en"
    
if __name__ == '__main__':
  unittest.main()