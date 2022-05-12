from Pages.base_page import BasePage
from Resources.locators import VisualizePageLocators

class VisualizePage(BasePage):
  def __init__(self, driver):
    super().__init__(driver)
    self.go_visualize()
  
  def possible_categories(self):
    div = self.driver.find_elements(*VisualizePageLocators.OPTIONS)
    labels = div[1].find_elements(*VisualizePageLocators.LABEL)
    label_text = []
    for x in labels:
      label_text.append(x.text.lstrip())
    return label_text
