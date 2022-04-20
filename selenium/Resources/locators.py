from selenium.webdriver.common.by import By

class BasePageLocators():
  NAV = (By.TAG_NAME, 'nav')
  NAV_ITEM = (By.CLASS_NAME, 'nav-item')

class HomePageLocators():
  ARTICLE = (By.TAG_NAME, 'article')
  LINK = (By.CLASS_NAME, 'institution-link')

class DataPageLocators():
  BUTTON = (By.CLASS_NAME, 'tableButtons')
  TABLE = (By.CLASS_NAME, 'med_table')
  BODY = (By.TAG_NAME, 'tbody')
  HEAD = (By.TAG_NAME, 'thead')
  COLUMN = (By.TAG_NAME, 'th')
  ROW = (By.TAG_NAME, 'tr')
  CELL = (By.TAG_NAME, 'td')
  SELECT = (By.CLASS_NAME, 'tableCheckboxColumn')
  RESULTS_PER_PAGE = (By.ID, 'topSelector')
