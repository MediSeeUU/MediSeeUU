import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverSetup(unittest.TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    self.driver.get("http://localhost:3000")
  
  def tearDown(self):
    self.driver.close()
    self.driver.quit()
