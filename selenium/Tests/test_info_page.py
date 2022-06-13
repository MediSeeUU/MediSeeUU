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
  
  # test if the page is correct
  def test_info_url(self):
    assert self.info_page.current_url() == "http://localhost:3000/info"

  # check if the infopage contains the 3 links with additional information
  def test_content(self):
    assert self.info_page.get_link(0) == "https://cbg-meb.nl/"
    assert self.info_page.get_link(1) == "https://www.ema.europa.eu/"
    assert self.info_page.get_link(2) == "https://ec.europa.eu/health/documents/community-register_en"
    
if __name__ == '__main__':
  unittest.main()
