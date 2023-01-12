import json
from datetime import date
from unittest import TestCase

import regex as re
from parameterized import parameterized

import scraping.utilities.definitions.attributes as attr
import scraping.utilities.config.__main__ as cf
from scraping.utilities.io.pathlib_extended import Path
from scraping.utilities.log import log_tools
from scraping.web_scraper import __main__ as web

data_path_str = "../tests/test_data_integration"
json_path = Path("web_scraper_tests/JSON")
scraping_root_path = Path.cwd().parent

# Different paths needed when running tests from the web_scraper folder
# instead of the parent tests folder
if Path.cwd().name == "web_scraper_tests":
    data_path_str = "../../tests/test_data_integration"
    json_path = Path("JSON")
    scraping_root_path = Path.cwd().parent.parent

data_path = Path(data_path_str)
data_path_local = data_path / "active_withdrawn"


def check_new_eu_numbers(self):
    """
    Check whether EU numbers in eu_number.json are equal to the eu_numbers of the medicines being downloaded.
    This should be the case, as all medicines are new, since they are downloaded for the first time in each test run.
    """

    # Find all files in the structure of `2022-01-01_eu_numbers-0.json`
    # Sort the list and grab the last file in the list. This is the latest eu_numbers file
    all_files = list(
        filter(lambda file: re.match(f"{date.today()}_eu_numbers_\\d.json", file.name),
               data_path.iterdir())
    )

    all_files.sort(key=lambda x: x.name)
    eu_numbers_file = all_files[-1]

    with open(eu_numbers_file) as f:
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
        cf.data_path = data_path_str
        cf.logging_path = f"{scraping_root_path}/tests/logs/log_files"

        json_path.rmdir_recursive(not_exist_ok=True)
        data_path.rmdir_recursive(not_exist_ok=True)

        log_tools.init_loggers()

        # exists_ok flag is off, we want to throw an error when the path exists beforehand
        data_path.mkdir()
        data_path_local.mkdir()
        json_path.mkdir()

    def setUp(self):
        """
        Create required folders for data and logs
        """
        data_path_local.rmdir_recursive()
        data_path_local.mkdir()

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
        web.main(cf.default_config,self.medicine_list)

    def run_ec_scraper(self):
        """
        Runs EC scraper and checks if everything works and correct files are created.
        """
        test_config = cf.off_config[cf.web_config]
        test_config[cf.web_scrape_ec] = True
        test_config[cf.web_download_refused] = True
        web.main(test_config,self.medicine_list)

        # check if data folder for eu_n exists and is filled
        medicine_folder = data_path_local / self.eu_n

        assert medicine_folder.exists(), f"Data folder for {self.eu_n} does not exist"

        assert medicine_folder.is_dir(), f"{medicine_folder} is not a directory"

        assert sum(1 for _ in medicine_folder.iterdir()) > 0, f"{medicine_folder} is empty"

        # If the size of the file is larger than two bytes, we assume the file has data
        assert (medicine_folder / f"{self.eu_n}_webdata.json").stat().st_size > 2, \
            f"webdata.json is empty for {self.eu_n}"

        # check if urls.json is empty
        assert (json_path / "urls.json").stat().st_size > 2, f"urls.json is empty"

    def run_ema_scraper(self):
        """
        Runs EMA scraper and checks if everything works and correct files are created.
        """
        test_config = cf.off_config[cf.web_config]
        test_config[cf.web_scrape_ema] = True
        web.main(test_config, self.medicine_list)

        with open(json_path / "urls.json") as f:
            url_dict = (json.load(f))[self.eu_n]

        assert all(x in list(url_dict.keys()) for x in
                   [attr.epar_url, attr.omar_url, attr.odwar_url, attr.other_ema_urls]), "ema urls not in urls.json"

    def run_download(self):
        """
        Runs download and checks if all files are downloaded and correct files are created.
        """
        test_config = cf.off_config[cf.web_config]
        test_config[cf.web_download] = True
        web.main(test_config, self.medicine_list)

        medicine_folder = data_path_local / self.eu_n

        # check if `filedates.json` exists
        assert (medicine_folder / f"{self.eu_n}_webdata.json").exists()

        # check if eu_numbers in eu_numbers.json equals all medicines, as all medicines should be new.
        check_new_eu_numbers(self)

        # check if all files from urls.json are downloaded:
        with open(json_path / "urls.json") as f:
            url_dict = (json.load(f))[self.eu_n]
        filecount = len(url_dict[attr.aut_url]) + len(url_dict[attr.smpc_url])

        if url_dict[attr.epar_url]:
            filecount += 1
        if url_dict[attr.omar_url]:
            filecount += 1
        if url_dict[attr.odwar_url]:
            filecount += 1
        for _ in url_dict[attr.other_ema_urls]:
            filecount += 1

        # Iterdir is a generator.
        # This is the most memory efficient way to sum a generator.
        assert sum(1 for _ in medicine_folder.iterdir()) == filecount + 1, "not all files are downloaded"

        # check `filedates.json` contents
        with open(medicine_folder / f"{self.eu_n}_webdata.json") as f:
            attr_dict = json.load(f)

        for file in medicine_folder.iterdir():
            if file.suffix == ".pdf":
                assert file.name in attr_dict[attr.filedates_web].keys(), f"{file} does not exist in filedates.json"

    def run_filter(self):
        """
        Runs filter_retry and checks if filter.txt is created
        """
        test_config = cf.off_config[cf.web_config]
        test_config[cf.web_run_filter] = True
        web.main(test_config, self.medicine_list)

        # check if filter.txt exists
        filter_path = scraping_root_path / "tests/logs/txt_files/filter.txt"

        assert filter_path.exists(), "filter.txt does not exist"

    @classmethod
    def tearDownClass(cls):
        """
        Runs after class is run, makes sure test data is deleted and backup data is set back to its original place
        """
        data_path.rmdir_recursive()
