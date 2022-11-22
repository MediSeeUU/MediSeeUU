import pytest
import os
from scraping.filter import pdf_filter
import fitz
import sys
from parameterized import parameterized

data_dir = "../test_data"
if "pdfscraper_tests" in os.getcwd():
    data_dir = "../../test_data"

# TODO: write filter tests
class TestFilter:
    @parameterized.expand([["", ""]])
    def test_check_for_no_text(self, pdf_name, status):
        assert True
        # file_path = os.path.join(data_dir, pdf_name.strip())
        #
        # pdf = fitz.open(file_path)
        # print(pdf)
        # if status.strip() == 'no_text':
        #     assert (pdf_filter.check_for_no_text(pdf))
        #
        # else:
        #     assert not (pdf_filter.check_for_no_text(pdf))
        # print("Testing pdf filter")
