from selenium.webdriver.common.by import By

# this file contains the locators of all pages
# these are needed to find the elements on the page

class BasePageLocators():
  NAV = (By.TAG_NAME, 'nav')
  NAV_ITEM = (By.CLASS_NAME, 'med-nav-item')
  LOGIN_NAV = (By.CLASS_NAME, 'med-nav-lowest')
  LOGIN_INPUT = (By.CLASS_NAME, 'med-credential-input')
  LOGIN_BUTTON = (By.CLASS_NAME, 'med-button-login')
  ACCOUNT_NAV = (By.CLASS_NAME, 'med-nav-account')

class InfoPageLocators():
  LINK = (By.CLASS_NAME, 'med-link')

class SearchLocators():
  SEARCH_BAR = (By.CLASS_NAME, 'med-text-input')
  BUTTON = (By.CLASS_NAME, 'med-search-button')

class TableLocators():
  TABLE = (By.CLASS_NAME, 'med-table')
  BODY = (By.TAG_NAME, 'tbody')
  HEAD = (By.TAG_NAME, 'thead')
  COLUMN = (By.TAG_NAME, 'th')
  ROW = (By.TAG_NAME, 'tr')
  CELL = (By.TAG_NAME, 'td')
  COLUMN_SELECT = (By.TAG_NAME, 'select')
  INFO = (By.TAG_NAME, 'i')
  ADD_COLUMN = (By.CLASS_NAME, 'bxs-plus-square')
  REMOVE_COLUMN = (By.CLASS_NAME, 'bxs-minus-square')
  SORT_COLUMN = (By.CLASS_NAME, 'med-table-header-sort')

class DataPageLocators():
  BUTTON = (By.CLASS_NAME, 'med-bx-button')
  SELECT = (By.CLASS_NAME, 'tableCheckboxColumn')
  RESULTS_PER_PAGE = (By.ID, 'med-result-count-selector')
  CLEAR_ALL = (By.CLASS_NAME, 'med-clear-all-button')
  RIGHT_ACTIONS = (By.CSS_SELECTOR, ".med-table-body-cell.med-table-narrow-column.med-column-right")
  NEXT_PAGE = (By.CLASS_NAME, 'bxs-chevron-right')
  PREV_PAGE = (By.CLASS_NAME, 'bxs-chevron-left')
  SELECTED_PAGE = (By.CLASS_NAME, 'med-page-selected')
  PAGES = (By.CLASS_NAME, 'med-no-select')
  BOTTOM_HOLDER = (By.CLASS_NAME, 'med-bottom-container-holder')

  class MenuLocators():
    FILTER_ITEM = (By.CLASS_NAME, 'med-table-menu-filter-item')
    ADD_FILTER = (By.CLASS_NAME, 'med-table-menu-add-filter')
    SELECT = (By.TAG_NAME, 'select')
    INPUT = (By.TAG_NAME, 'input')
    SORT_ITEM = (By.CLASS_NAME, 'med-table-menu-sort-item')
    APPLY = (By.CLASS_NAME, 'med-table-menu-apply-button')
  
  class SaveLocators():
    SAVE_INPUT = (By.CLASS_NAME, 'med-text-input')
    SAVE_BUTTON = (By.CLASS_NAME, 'accept')

class VisualizePageLocators():
  OPTIONS = (By.CLASS_NAME, 'country-options')
  LABEL = (By.TAG_NAME, 'label')

class DetailedPageLocators():
  DETAIL_ITEM = (By.CLASS_NAME, 'med-info-detail')
  DETAIL_NAME = (By.CLASS_NAME, 'med-info-detail-name')
  DETAIL_VALUE = (By.CLASS_NAME, 'med-info-detail-value')

class AccountPageLocators():
  SAVED_SELECTION = (By.CLASS_NAME, 'med-saved-selection')
  SAVED_NAME = (By.CLASS_NAME, 'med-selection-name')
  SAVED_COUNT = (By.CLASS_NAME, 'med-selection-count')
  SAVED_SELECT = (By.CLASS_NAME, 'med-selection-select')
