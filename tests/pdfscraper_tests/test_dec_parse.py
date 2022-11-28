from unittest import TestCase
import os
import regex as re
import fitz
import datetime
import scraping.file_parser.pdf_parser.parsers.dec_parser as dec_parser
import scraping.file_parser.pdf_parser.pdf_helper as pdf_helper

test_data_loc = "../test_data"
if "pdfscraper_tests" in os.getcwd():
    test_data_loc = "../../test_data"
dec_txt = []
percentage_str = "Percentage found: "


# Tests all functions of EPAR parser with all XML files
class TestDecParse(TestCase):
    """
    Class that contains the unit tests for scraping.file_parser.pdf_parser.parsers.dec_parser
    """
    @classmethod
    def setUpClass(cls):
        """
        Prepare a list of XML files in the global variable xml_bodies
        """
        files = []
        for folder in os.listdir(test_data_loc):
            if not os.path.isdir(os.path.join(test_data_loc, folder)):
                continue
            for file in os.listdir(os.path.join(test_data_loc, folder)):
                path = os.path.join(test_data_loc, folder, file)
                if os.path.isfile(path):
                    files.append(path)
        dec_files = [file for file in files if "dec_0" in file and ".pdf" in file]
        # Get content of PDF files
        for dec_file in dec_files:
            try:
                pdf = fitz.open(dec_file)
                txt = pdf_helper.get_text_str(pdf)
                pdf.close()
                dec_txt.append((txt, dec_file))
            except fitz.fitz.FileDataError:
                print("EC Test: failed to open PDF file " + dec_file)

    # eu_prime_initial
    def test_get_date(self):
        """
        Testing format of get_date function
        """
        not_found_count = 0
        for txt, filename in dec_txt:
            output = dec_parser.dec_get_date(txt)
            self.assertTrue((isinstance(output, str) or isinstance(output, datetime.datetime)))
            if output == datetime.datetime(1980, 1, 1, 0, 0):
                not_found_count += 1
                print(f"{filename} date not found")
            if isinstance(output, datetime.datetime):
                self.assertGreater(datetime.datetime(2050, 1, 1, 0, 0), output)
                self.assertGreater(output, datetime.datetime(1979, 1, 1, 0, 0))
            if isinstance(output, str):
                self.assertTrue(output == 'Date is blank')
        percentage_found = (len(dec_txt) - not_found_count) / len(dec_txt) * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        print(f"Amount not found: {not_found_count}")
        self.assertGreater(percentage_found, 89)

    def test_get_od_comp_date(self):
        """
        Testing format of get_od_comp_date function
        """
        not_found_count = 0
        orphan_count = 0
        for txt, filename in dec_txt:
            if '_o_' in filename:
                orphan_count += 1
                output = dec_parser.dec_get_od_comp_date(txt)
                self.assertTrue(isinstance(output, datetime.datetime))
                if output == datetime.datetime(1980, 1, 1, 0, 0):
                    not_found_count += 1
                    print(f"{filename} date not found")
                else:
                    self.assertGreater(datetime.datetime(2050, 1, 1, 0, 0), output)
                    self.assertGreater(output, datetime.datetime(1979, 1, 1, 0, 0))
        percentage_found = (orphan_count - not_found_count) / orphan_count * 100
        print(percentage_str + str(round(percentage_found, 2)) + '%')
        print(f"Amount not found: {not_found_count}")
        self.assertGreater(percentage_found, 75)
