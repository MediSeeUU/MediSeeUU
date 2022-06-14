import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# setup selenium webdriver
class WebDriverSetup(unittest.TestCase):
  # setup tests
  def setUp(self):
    # create remote headless chrome instance if the test is run in a CI environment
    if os.getenv('CI', False):
      options = webdriver.ChromeOptions()
      options.add_argument('--headless')
      options.add_argument('--no-sandbox')
      options.add_argument('--no-gpu')
      self.driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        options=options
      )
    else:
      options = webdriver.ChromeOptions()
      self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # set window size, initial site location and an implicit wait for the data
    self.driver.set_window_size(1920, 1080)
    self.driver.get("http://localhost:3000")
    self.driver.implicitly_wait(10)
  
  # tear down tests
  def tearDown(self):
    self.driver.close()
    self.driver.quit()
