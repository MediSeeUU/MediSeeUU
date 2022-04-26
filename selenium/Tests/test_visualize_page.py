import sys
import os
import unittest
import random
import time

base_dir = os.path.dirname(__file__) or '.'
sys.path.append("..")

from WebDriverSetup import WebDriverSetup
from Pages.visualize_page import VisualizePage

class TestVisualizePage(WebDriverSetup):
  def setUp(self):
    super().setUp()
    self.visualize_page = VisualizePage(self.driver)
  
  # test if the page is correct
  def test_visualize_url(self):
    assert self.visualize_page.current_url() == "http://localhost:3000/visualizations"

if __name__ == '__main__':
  unittest.main()
