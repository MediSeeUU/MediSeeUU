from unittest import TestCase
import os
import shutil
import json

from scraping.pdf_parser import __main__ as pdf_parser
from scraping.pdf_parser import parsed_info_struct as pis
from scraping.utilities.log import log_tools
from scraping.utilities.io import safe_io
import scraping.utilities.web.config_objects as config

data_path = "../tests/test_data"
if "pdf_parser_tests" in os.getcwd():
    data_path = "../../tests/test_data"
parent_path = "/".join((data_path.split('/')[:-2]))
active_withdrawn_dir = f"{data_path}/active_withdrawn"


class TestPdfParser(TestCase):
    """
    Class that runs PDF parser, mostly checks if files get downloaded
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the class to make sure the integration test can run without changing existing data.
        """
        safe_io.delete_folder(f"{parent_path}/tests/logs/txt_files")
        safe_io.delete_folder(f"{parent_path}/tests/logs/log_files")

        config.default_path_data = data_path
        config.default_path_logging = f"{parent_path}/tests/logs/log_files"

        log_tools.init_loggers()

    def test_pdf_parser_no_checks(self):
        """
        Runs PDF parser and passes if no errors occur.
        """
        pdf_parser.main(data_path, parse_all=False)
        pdf_parser.main(data_path, parse_all=True)

    def test_pdf_parser_with_checks(self):
        """
        Runs PDF parser and checks whether the amount of parsed files equals the number of PDF files in the medicine
        folder
        """
        pdf_parser.main(data_path, parse_all=True)
        for folder in os.listdir(active_withdrawn_dir):
            medicine_path = f"{active_withdrawn_dir}/{folder}"
            files = [file for file in os.listdir(medicine_path) if os.path.isfile(os.path.join(medicine_path, file))
                     and "other" not in file]
            annex_files = [file for file in files if "anx" in file and ".xml" in file]
            decision_files = [file for file in files if "dec" in file and ".xml" not in file]
            epar_files = [file for file in files if
                          ("public-assessment-report" in file or "procedural-steps-taken" in file or "epar" in file)
                          and ".xml" in file]
            omar_files = [file for file in files if ("omar" in file or "orphan" in file) and ".xml" in file]
            pdf_json_path = f"{medicine_path}/{folder}_pdf_parser.json"
            assert os.path.exists(pdf_json_path)

            with open(pdf_json_path) as pdf_json:
                pdf_data: dict = json.load(pdf_json)
                anx_count = len(pdf_data["annexes"])
                dec_count = len(pdf_data["decisions"])
                epar_count = len(pdf_data["epars"])
                omar_count = len(pdf_data["omars"])
                for files, count in zip([annex_files, decision_files, epar_files, omar_files],
                                        [anx_count, dec_count, epar_count, omar_count]):
                    # There should be an entry in the pdf_parser.json for each file
                    assert len(files) == count
