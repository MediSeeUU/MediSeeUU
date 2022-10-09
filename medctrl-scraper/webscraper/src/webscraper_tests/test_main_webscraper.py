from unittest import TestCase, mock
from pathlib import Path
import sys

sys.path.append(".")



# TODO: write tests for __main__.py
class Test(TestCase):
    # TODO: find a way to mock the writing to the file
    def test_get_urls(self):
        path = Path("./data/CSV/annexes.csv")
        self.assertTrue(path.is_file())
        self.assertTrue(path.parent.is_dir())

    def test_download_pdfs(self):
        self.fail()

    def test_read_csv_files(self):
        self.fail()

    def test_run_parallel(self):
        self.fail()
