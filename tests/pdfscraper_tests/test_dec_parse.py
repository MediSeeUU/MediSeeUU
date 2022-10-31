from unittest import TestCase
import os
import regex as re
import fitz
import datetime
import scraping.pdf_module.pdf_scraper.parsers.dec_parse as dec_parse

test_data_loc = "../../data"
dec_txt = []
percentage_str = "Percentage found: "


# Tests all functions of EPAR parser with all XML files
class TestEparParse(TestCase):
    def setUp(self):
        # Prepare a list of XML files
        files = [file for file in os.listdir(test_data_loc) if os.path.isfile(os.path.join(test_data_loc, file))]
        dec_files = [file for file in files if "dec" and ".pdf" and "_0" in file]
        # Get XML bodies, assuming there are XML files
        for dec_file in dec_files:
            dec_path = os.path.join(test_data_loc, dec_file)
            pdf = fitz.open(dec_path)
            txt = dec_parse.get_txt_from_pdf(pdf)
            pdf.close()
            dec_txt.append(txt)

    # eu_prime_initial
    def test_get_prime(self):
        # Call get_prime
        for txt in dec_txt:
            output = dec_parse.dec_get_date(txt)
            self.assertTrue(isinstance(output, datetime.datetime))


    # # ema_procedure_start_initial
    # def test_get_date(self):
    #     found_count = 0
    #     # Call get_date
    #     for xml_body in xml_bodies:
    #         output = epar_parse.get_date(xml_body)
    #         if output != "no_date_found":
    #             found_count += 1
    #             day = re.search(r"\d{2}/", output)[0][:2].strip()
    #             month = re.search(r"/\d{2}/", output)[0][1:3].strip()
    #             year = re.search(r"\d{4}", output)[0].strip()
    #             self.check_date(day, month, year)
    #     percentage_found = found_count / len(xml_bodies) * 100
    #     print(percentage_str + str(round(percentage_found, 2)) + '%')
    #     self.assertGreater(percentage_found, 90)

    # # chmp_opinion_date
    # def test_get_opinion_date(self):
    #     found_count = 0
    #     # Call get_opinion_date
    #     for xml_body in xml_bodies:
    #         output = epar_parse.get_opinion_date(xml_body)
    #         if output != "no_chmp_found":
    #             found_count += 1
    #             day = re.search(r"\d{2}/", output)[0][:2].strip()
    #             month = re.search(r"/\d{2}/", output)[0][1:3].strip()
    #             year = re.search(r"\d{4}", output)[0].strip()
    #             self.check_date(day, month, year)
    #     percentage_found = found_count / len(xml_bodies) * 100
    #     print(percentage_str + str(round(percentage_found, 2)) + '%')
    #     self.assertGreater(percentage_found, 90)

    # # Check for reasonable dates
    # def check_date(self, day, month, year):
    #     self.assertGreater(int(year), 1900)
    #     # Make sure to check this in the future :D
    #     self.assertGreater(3000, int(year))
    #     self.assertGreater(int(month), 0)
    #     self.assertGreater(13, int(month))
    #     self.assertGreater(int(day), 0)
    #     self.assertGreater(32, int(day))

    # # eu_legal_basis
    # def test_get_legal_basis(self):
    #     found_count = 0
    #     # Call get_legal_basis
    #     for xml_body in xml_bodies:
    #         output = epar_parse.get_legal_basis(xml_body)
    #         if output != "no_legal_basis":
    #             found_count += 1
    #             self.assertGreater(len(output), 0)
    #             for a in output:
    #                 self.assertIn("article", a)
    #     percentage_found = found_count / len(xml_bodies) * 100
    #     print(percentage_str + str(round(percentage_found, 2)) + '%')
    #     self.assertGreater(percentage_found, 90)

    # # eu_prime_initial
    # def test_get_prime(self):
    #     yes_exists = False
    #     # Call get_prime
    #     for xml_body in xml_bodies:
    #         output = epar_parse.get_prime(xml_body)
    #         if output == "yes":
    #             yes_exists = True
    #         self.assertIn(output, 'yesno')
    #     self.assertTrue(yes_exists)
