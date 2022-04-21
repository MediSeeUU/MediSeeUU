from selenium.webdriver.common.by import By

class BasePageLocators():
  NAV = (By.TAG_NAME, 'nav')
  NAV_ITEM = (By.CLASS_NAME, 'nav-item')

class HomePageLocators():
  ARTICLE = (By.TAG_NAME, 'article')
  LINK = (By.CLASS_NAME, 'institution-link')

class TableLocators():
  TABLE = (By.CLASS_NAME, 'med_table')
  BODY = (By.TAG_NAME, 'tbody')
  HEAD = (By.TAG_NAME, 'thead')
  COLUMN = (By.TAG_NAME, 'th')
  ROW = (By.TAG_NAME, 'tr')
  CELL = (By.TAG_NAME, 'td')
  COLUMN_SELECT = (By.TAG_NAME, 'select')
  INFO = (By.TAG_NAME, 'i')

class DataPageLocators():
  BUTTON = (By.CLASS_NAME, 'tableButtons')
  SELECT = (By.CLASS_NAME, 'tableCheckboxColumn')
  RESULTS_PER_PAGE = (By.ID, 'topSelector')
  SELECTED_PAGE = (By.CLASS_NAME, 'lb-pageCount_selected')
  NEXT_PAGE = (By.CLASS_NAME, 'bxs-chevron-right')
  PREV_PAGE = (By.CLASS_NAME, 'bxs-chevron-left')

  class MenuLocators():
    FILTER_ITEM = (By.CLASS_NAME, 'filter-item')
    ADD_FILTER = (By.CLASS_NAME, 'add')
    SELECT = (By.TAG_NAME, 'select')
    INPUT = (By.TAG_NAME, 'input')
    SORT_ITEM = (By.CLASS_NAME, 'sort-item')
    APPLY = (By.CLASS_NAME, 'apply')

class VisualizePageLocators():
  OPTIONS = (By.CLASS_NAME, 'country-options')
  LABEL = (By.TAG_NAME, 'label')
