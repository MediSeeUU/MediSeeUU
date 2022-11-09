import pytest
import os
from scraping.filter import pdf_filter
import fitz
import sys


class TestFilter:
    def test_check_for_no_text(self, pdf_name, status):
        file_path = os.path.join(data_dir, pdf_name.strip())

        pdf = fitz.open(file_path)
        print(pdf)
        if status.strip() == 'no_text':
            assert (pdf_filter.check_for_no_text(pdf))

        else:
            assert not (pdf_filter.check_for_no_text(pdf))
        print("Testing pdf filter")
