"""
| The scraper package defines the view for the scraper module to upload new medicines.
"""
# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# from .router import url_patterns
from .human_medicine_info import Human_medicine_info
from .orphan_medicine_info import Orphan_medicine_info
from .medicine_info_json import get_medicine_info
