import os.path as path
import os
import shutil
import json
from pathlib import Path
from unittest import TestCase
from datetime import date
from scraping.web_scraper import __main__ as web
import scraping.log_setup as log_setup
from parameterized import parameterized

data_path = "../test_data"
if "web_scraper_tests" in os.getcwd():
    data_path = "../../test_data"

if not path.isdir(data_path):
    os.mkdir(data_path)

json_path = "web_scraper_tests/"
if "web_scraper_tests" in os.getcwd():
    json_path = ""

parent_path = "/".join((data_path.split("/")[:-1])) + "/"


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

    # Rename data to data_old
    @classmethod
    def setUpClass(cls):
        """
        Set up the class to make sure the integration test can run without changing existing data.
        """
        log_setup.init_loggers(f"{parent_path}/scraping")
        if not os.path.exists(f"{data_path}_old"):
            os.rename(data_path, f"{data_path}_old")
        if not path.isdir(data_path):
            os.mkdir(data_path)
        Path(f"{json_path}JSON").mkdir(parents=True, exist_ok=True)

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
        shutil.rmtree(data_path)
        os.mkdir(data_path)

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
        shutil.rmtree(data_path)
        os.mkdir(data_path)

        self.parallel = parallel
        self.medicine_list = medicine_list
        web.main(data_filepath=data_path, scrape_ec=True, scrape_ema=True, download_files=True,
                 download_refused_files=True, run_filter=True, use_parallelization=self.parallel,
                 medicine_list=self.medicine_list)

    def run_ec_scraper(self):
        """
        Runs EC scraper and checks if everything works and correct files are created.
        """
        web.main(data_filepath=data_path, scrape_ec=True, scrape_ema=False, download_files=False,
                 download_refused_files=True, run_filter=False, use_parallelization=self.parallel,
                 medicine_list=self.medicine_list)
        # check if data folder for eu_n exists and is filled
        data_folder = f"{data_path}/{self.eu_n}"
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
        web.main(data_filepath=data_path, scrape_ec=False, scrape_ema=True, download_files=False, run_filter=False,
                 use_parallelization=self.parallel, medicine_list=self.medicine_list)
        with open(f"{json_path}JSON/urls.json") as f:
            url_dict = (json.load(f))[self.eu_n]
        assert all(x in list(url_dict.keys()) for x in ['epar_url', 'omar_url', 'odwar_url', 'other_ema_urls']), \
            "ema urls not in urls.json"

    def run_download(self):
        """
        Runs download and checks if all files are downloaded and correct files are created.
        """
        web.main(data_filepath=data_path, scrape_ec=False, scrape_ema=False, download_files=True, run_filter=False,
                 use_parallelization=self.parallel, medicine_list=self.medicine_list)

        # check if `filedates.json` exists
        data_folder = f"{data_path}/{self.eu_n}"
        assert path.exists(f"{data_folder}/{self.eu_n}_filedates.json")

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

        assert len(os.listdir(data_folder)) == filecount + 2, "not all files are downloaded"

        # check `filedates.json` contents
        with open(f"{data_folder}/{self.eu_n}_filedates.json") as f:
            filedates_dict = json.load(f)
        for file in os.listdir(data_folder):
            if ".pdf" in file:
                assert file in filedates_dict.keys(), f"{file} does not exist in filedates.json"

    def run_filter(self):
        """
        Runs filter_retry and checks if filter.txt is created
        """
        web.main(data_filepath=data_path, scrape_ec=False, scrape_ema=False, download_files=False, run_filter=True,
                 use_parallelization=self.parallel, medicine_list=self.medicine_list)
        # check if filter.txt exists
        assert path.exists("filter.txt"), "filter.txt does not exist"

    @classmethod
    def tearDownClass(cls):
        """
        Runs after class is run, makes sure test data is deleted and backup data is set back to its original place
        """
        shutil.rmtree(data_path)
        os.rename(f"{data_path}_old", data_path)
        if os.path.exists('filter.txt'):
            os.remove('filter.txt')
        if os.path.exists('no_english_available.txt'):
            os.remove('no_english_available.txt')
