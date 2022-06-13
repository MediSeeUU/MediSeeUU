from Pages.base_page import BasePage
from Resources.locators import VisualizePageLocators

# visualization page that visualizes the selected data by the use of charts
class VisualizePage(BasePage):
  def __init__(self, driver):
    super().__init__(driver)
    # navigate to the visualization page
    self.go_visualize()
  
  # returns the categories that can be selected on the specified axis
  def possible_categories(self, axis):
    div = self.driver.find_elements(*VisualizePageLocators.OPTIONS)
    labels = div[axis].find_elements(*VisualizePageLocators.LABEL)
    label_text = []
    for x in labels:
      label_text.append(x.text.lstrip())
    return label_text
