from unittest import TestCase
import os

from scraping.transformer import __main__ as transformer
from scraping.utilities.log import log_tools
from scraping.utilities.io import safe_io
import scraping.utilities.web.config_objects as config

data_path = "../tests/test_data"
if "transformer_tests" in os.getcwd():
    data_path = "../../tests/test_data"
parent_path = "/".join((data_path.split('/')[:-2]))
active_withdrawn_dir = f"{data_path}/active_withdrawn"


class TestTransformer(TestCase):
    """
    Class that runs the transformer, mostly checks if a transformed.json gets created for each combined.json.
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

    def test_transformer_no_checks(self):
        """
        Runs transformer and passes if no errors occur.
        """
        transformer.main(data_path)

    def test_pdf_test_transformer_with_checks(self):
        """
        Runs transformer and passes if there exists a combined.json and transformed.json for each file after running
        the transformer.
        """
        transformer.main(data_path)
        for folder in os.listdir(active_withdrawn_dir):
            medicine_path = f"{active_withdrawn_dir}/{folder}"
            combined_path = f"{medicine_path}/{folder}_combined.json"
            assert os.path.exists(combined_path)
            transformed_path = f"{medicine_path}/{folder}_transformed.json"
            assert os.path.exists(transformed_path)
