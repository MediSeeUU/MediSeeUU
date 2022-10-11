import pytest
import os
data_dir = 'PDF_scraper/text_scraper/data'


class TestFilter(pdf_name):
    file_path = os.path.join(data_dir, pdf_name)

    def test_pdf_filter(pdf):
        print("Testing pdf filter")