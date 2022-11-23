from unittest import TestCase
import pytest
import os
from scraping.filter import filter
import fitz
import sys
from distutils.dir_util import copy_tree
import shutil

test_data_loc = "../../test_data_filter"
test_data_filter_loc = "../../test_data_filter_temp"


def get_removed_files() -> set[str]:
    """
    Returns:
        set[str]: Set of files that are present in original data directory, but not in the filtered directory.
    """
    original: set = set()
    filtered: set = set()
    for folder in os.listdir(test_data_loc):
        folder_orig = os.path.join(test_data_loc, folder)
        folder_filter = os.path.join(test_data_filter_loc, folder)
        original = original.union(set(os.listdir(folder_orig)))
        filtered = filtered.union(set(os.listdir(folder_filter)))
    return original.difference(filtered)


class TestFilter(TestCase):
    """
    Class to test Filter using integration tests.
    """
    def setUp(self):
        """
        Set up the class to make sure the integration test can run without changing existing data.
        Copies test_data folder to test_data_filter [since filter removes files]
        """
        copy_tree(test_data_loc, test_data_filter_loc)

    def test_pdf_filter_length(self):
        """
        Checks whether the length of filter.txt is equal to the number of removed files
        """
        filter.filter_all_pdfs(test_data_filter_loc)
        with open("filter.txt", 'r', encoding="utf-8") as file:
            filtered_files = file.read().split("\n")
        filtered_count = len([file for file in filtered_files if len(file) > 1])
        removed_files = get_removed_files()
        print(removed_files)
        self.assertEqual(filtered_count, len(removed_files))

    def test_pdf_filter_writing(self):
        """
        Checks whether all files in filter.txt have been removed, and all removed files are in filter.txt
        """
        filter.filter_all_pdfs(test_data_filter_loc)
        with open("filter.txt", 'r', encoding="utf-8") as file:
            filtered_files = file.read().split("\n")
        filtered_filenames = [file.split('@')[0] for file in filtered_files if file != '']
        removed_files = get_removed_files()
        self.assertEqual(set(filtered_filenames), removed_files)

    @classmethod
    def tearDownClass(cls):
        """
        Remove copy of test_data_filter folder at end of testing
        """
        if os.path.exists(test_data_filter_loc):
            shutil.rmtree(test_data_filter_loc)
