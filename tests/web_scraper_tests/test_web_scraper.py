import json
import os
import os.path as path
import shutil
from datetime import date
from pathlib import Path
from unittest import TestCase

import scraping.utilities.web.config_objects as config
from scraping.web_scraper import __main__ as web
from scraping.utilities.log import log_tools
from scraping.utilities.io import safe_io
from parameterized import parameterized

data_path = "../test_data"
if "web_scraper_tests" in os.getcwd():
    data_path = "../../test_data"
data_path_local = f"{data_path}/active_withdrawn"

safe_io.create_folder(data_path)

json_path = "web_scraper_tests/"
if "web_scraper_tests" in os.getcwd():
    json_path = ""

parent_path = "/".join((data_path.split('/')[:-1]))
filter_path = f"{parent_path}/tests/logs/txt_files/filter.txt"


def check_new_eu_numbers(self):
    """
    Check whether EU numbers in eu_number.json are equal to the eu_numbers of the medicines being downloaded.
    This should be the case, as all medicines are new, since they are downloaded for the first time in each test run.
    """
    eu_numbers_path = ""
    eu_numbers_base_path = f"{data_path}/{date.today()}_eu_numbers"

    file_exists = True
    i = 0
    while file_exists:
        eu_numbers_path = f"{eu_numbers_base_path}_{i}.json"
        i += 1
        file_exists = os.path.exists(f"{eu_numbers_base_path}_{i}.json")
    with open(eu_numbers_path) as f:
        eu_numbers = set(json.load(f))

    self.assertEqual(self.eu_numbers, eu_numbers)


class TestWebScraper(TestCase):
    """
    Class that runs web, mostly checks if files get downloaded
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the class to make sure the integration test can run without changing existing data.
        """
        config.default_path_data = data_path
        config.default_path_logging = f"{parent_path}/tests/logs/log_files"

        log_files_folder = f"{parent_path}/tests/logs/log_files"
        txt_files_folder = f"{parent_path}/tests/logs/txt_files"
        safe_io.delete_folder(log_files_folder)
        safe_io.delete_folder(txt_files_folder)

        log_tools.init_loggers()

        safe_io.rename(data_path, f"{data_path}_old")
        safe_io.create_folder(data_path)
        safe_io.create_folder(data_path_local)

        Path(f"{json_path}JSON").mkdir(parents=True, exist_ok=True)

    def setUp(self):
        """
        Create required folders for data and logs
        """
        safe_io.delete_folder(data_path_local)
        safe_io.create_folder(data_path_local)

    medicine_list_checks = \
        [('https://ec.europa.eu/health/documents/community-register/html/h273.htm', 'EU-1-04-273', 0, 'h273'),
         ('https://ec.europa.eu/health/documents/community-register/html/h283.htm', 'EU-1-04-283', 1, 'h283'),
         ('https://ec.europa.eu/health/documents/community-register/html/o005.htm', 'EU-3-00-005', 2, 'o005'),
         ('https://ec.europa.eu/health/documents/community-register/html/o101.htm', 'EU-3-02-101', 3, 'o101'),
         ('https://ec.europa.eu/health/documents/community-register/html/h1587.htm', 'EU-1-21-1587', 0, 'h1587')]

    @parameterized.expand([[True, medicine_list_checks], [False, medicine_list_checks]])
    def test_run_web_check_all(self, parallel, medicine_codes):
        """
        Runs webscraper and checks output in between different scripts
        Args:
            parallel: if web should run parallel or not
            medicine_codes: The medicine that is tested
        """
        self.parallel = parallel
        self.medicine_list = medicine_codes
        self.eu_n = self.medicine_list[0][1]
        self.eu_numbers = set([x[1] for x in self.medicine_list_checks])
        self.run_ec_scraper()
        self.run_ema_scraper()
        self.run_download()
        self.run_filter()

    @parameterized.expand([[True, medicine_list_checks], [False, medicine_list_checks]])
    def test_run_web_no_checks(self, parallel, medicine_list):
        """
        Runs webscraper and passes if no errors occur.
        Args:
            parallel: if web should run parallel or not
            medicine_list: The medicine that is tested
        """
        self.parallel = parallel
        self.medicine_list = medicine_list
        web.main(config.WebConfig().run_all().supply_medicine_list(self.medicine_list))

    def run_ec_scraper(self):
        """
        Runs EC scraper and checks if everything works and correct files are created.
        """
        web.main(config.WebConfig().run_custom(scrape_ec=True, download_refused=True)
                                   .set_parallel(self.parallel)
                                   .supply_medicine_list(self.medicine_list))

        # check if data folder for eu_n exists and is filled
        data_folder = f"{data_path_local}/{self.eu_n}"
        assert path.exists(data_folder), f"data folder for {self.eu_n} does not exist"
        assert path.isdir(data_folder), f"{data_folder} is not a directory"
        assert len(os.listdir(data_folder)) > 0, f"{data_folder} is empty"
        # check if webdata is empty
        assert path.getsize(f"{data_folder}/{self.eu_n}_webdata.json") > 2, f"webdata.json is empty for {self.eu_n}"
        # check if urls.json is empty
        assert path.getsize(f"{json_path}JSON/urls.json") > 2, f"urls.json is empty"

    def run_ema_scraper(self):
        """
        Runs EMA scraper and checks if everything works and correct files are created.
        """
        web.main(config.WebConfig().run_custom(scrape_ema=True)
                                   .set_parallel(self.parallel)
                                   .supply_medicine_list(self.medicine_list))

        with open(f"{json_path}JSON/urls.json") as f:
            url_dict = (json.load(f))[self.eu_n]
        assert all(x in list(url_dict.keys()) for x in ['epar_url', 'omar_url', 'odwar_url', 'other_ema_urls']), \
            "ema urls not in urls.json"

    def run_download(self):
        """
        Runs download and checks if all files are downloaded and correct files are created.
        """
        web.main(config.WebConfig().run_custom(download=True)
                                   .set_parallel(self.parallel)
                                   .supply_medicine_list(self.medicine_list))

        data_folder = f"{data_path_local}/{self.eu_n}"

        # check if eu_numbers in eu_numbers.json equals all medicines, as all medicines should be new.
        check_new_eu_numbers(self)

        # check if all files from urls.json are downloaded:
        with open(f"{json_path}JSON/urls.json") as f:
            url_dict = (json.load(f))[self.eu_n]
        filecount = len(url_dict["aut_url"]) + len(url_dict["smpc_url"])

        if url_dict["epar_url"]:
            filecount += 1
        if url_dict["omar_url"]:
            filecount += 1
        if url_dict["odwar_url"]:
            filecount += 1
        for _ in url_dict["other_ema_urls"]:
            filecount += 1
        print(url_dict)
        print(os.listdir(data_folder))
        print(len(os.listdir(data_folder)))
        assert len(os.listdir(data_folder)) == filecount + 1, "not all files are downloaded"
        # check `filedates contents
        with open(f"{data_folder}/{self.eu_n}_webdata.json") as f:
            attr_dict = json.load(f)
        for file in os.listdir(data_folder):
            if ".pdf" in file:
                assert file in attr_dict["filedates"].keys(), f"{file} does not exist in filedates.json"

    def run_filter(self):
        """
        Runs filter_retry and checks if filter.txt is created
        """
        web.main(config.WebConfig().run_custom(filtering=True)
                                   .set_parallel(self.parallel)
                                   .supply_medicine_list(self.medicine_list))

        # check if filter.txt exists
        assert path.exists(filter_path), "filter.txt does not exist"

    @classmethod
    def tearDownClass(cls):
        """
        Runs after class is run, makes sure test data is deleted and backup data is set back to its original place
        """
        safe_io.delete_folder(data_path)
        safe_io.rename(f"{data_path}_old", data_path)
