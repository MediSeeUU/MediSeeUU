import pytest
import os
import pdf_filter
import fitz
import sys

sys.path.append("..")  # Adds higher directory to python modules path.

data_dir = 'PDF_scraper/text_scraper/data'
f1 = open('tests/emar_list.txt', 'r', encoding="utf-8")
f2 = open('tests/statuses_emar.txt', 'r', encoding="utf-8")
pdfs = f1.readlines()
statuses = f2.readlines()

@pytest.mark.parametrize('pdf_name,status', zip(pdfs, statuses))
class TestFilter:
    def test_check_for_no_text(self, pdf_name, status):
        file_path = os.path.join(data_dir, pdf_name)
        pdf = fitz.open(file_path)
        if status == 'no_text':
            assert (pdf_filter.check_for_no_text(pdf))
        else:
            assert (pdf_filter.check_for_no_text(pdf))
        print("Testing pdf filter")
