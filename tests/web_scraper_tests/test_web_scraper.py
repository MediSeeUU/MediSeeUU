import os.path as path
import os
import shutil
import json
from unittest import TestCase
from scraping.web_scraper import __main__ as web
from parameterized import parameterized

data_path = "../../data"
if not path.isdir(data_path):
    os.mkdir(data_path)


class TestWebScraper(TestCase):
    """
    Class that runs web, mostly checks if files get downloaded
    """
    # Rename data to data_old
    @classmethod
    def setUpClass(cls):
        os.rename(data_path, f"{data_path}_old")
        os.mkdir(data_path)

    @parameterized.expand([[True, [('https://ec.europa.eu/health/documents/community-register/html/h273.htm',
                                    'EU-1-04-273', 0, 'h273')]],
                           [False, [('https://ec.europa.eu/health/documents/community-register/html/h273.htm',
                                     'EU-1-04-273', 0, 'h273')]],
                           [True, [('https://ec.europa.eu/health/documents/community-register/html/h283.htm',
                                    'EU-1-04-283', 1, 'h283')]],
                           [True, [('https://ec.europa.eu/health/documents/community-register/html/o005.htm',
                                    'EU-3-00-005', 2, 'o005')]],
                           [True, [('https://ec.europa.eu/health/documents/community-register/html/o101.htm',
                                    'EU-3-02-101', 3, 'o101')]],
                           [True, [('https://ec.europa.eu/health/documents/community-register/html/h131.htm',
                                    'EU-1-00-131', 1, 'h131')]]])
    def test_run_web_check_all(self, parallel, medicine_codes):
        shutil.rmtree(data_path)
        os.mkdir(data_path)

        self.parallel = parallel
        self.medicine_codes = medicine_codes
        self.eu_n = self.medicine_codes[0][1]
        self.run_ec_scraper()
        self.run_ema_scraper()
        #self.run_download()
        #self.run_filter()

        shutil.rmtree('JSON')

    @parameterized.expand([[True, [('https://ec.europa.eu/health/documents/community-register/html/h273.htm',
                                    'EU-1-04-273', 0, 'h273')]],
                           [False, [('https://ec.europa.eu/health/documents/community-register/html/h273.htm',
                                     'EU-1-04-273', 0, 'h273')]],
                           [True, [('https://ec.europa.eu/health/documents/community-register/html/h283.htm',
                                    'EU-1-04-283', 1, 'h283')]],
                           [False, [('https://ec.europa.eu/health/documents/community-register/html/h283.htm',
                                     'EU-1-04-283', 1, 'h283')]],
                           [True, [('https://ec.europa.eu/health/documents/community-register/html/o005.htm',
                                    'EU-3-00-005', 2, 'o005')]],
                           [False, [('https://ec.europa.eu/health/documents/community-register/html/o005.htm',
                                     'EU-3-00-005', 2, 'o005')]],
                           [True, [('https://ec.europa.eu/health/documents/community-register/html/o101.htm',
                                    'EU-3-02-101', 3, 'o101')]],
                           [False, [('https://ec.europa.eu/health/documents/community-register/html/o101.htm',
                                     'EU-3-02-101', 3, 'o101')]],
                           [True, [('https://ec.europa.eu/health/documents/community-register/html/h131.htm',
                                    'EU-1-00-131', 1, 'h131')]],
                           [False, [('https://ec.europa.eu/health/documents/community-register/html/h131.htm',
                                     'EU-1-00-131', 1, 'h131')]]])
    def test_run_web_no_checks(self, parallel, medicine_codes):
        shutil.rmtree(data_path)
        os.mkdir(data_path)

        self.parallel = parallel
        self.medicine_codes = medicine_codes
        web.main(data_filepath=data_path, scrape_ec=True, scrape_ema=True, download_files=True, run_filter=True,
                 use_parallelization=self.parallel, medicine_codes=self.medicine_codes)

        shutil.rmtree('JSON')

    def run_ec_scraper(self):
        web.main(data_filepath=data_path, scrape_ec=True, scrape_ema=False, download_files=False, run_filter=False,
                 use_parallelization=self.parallel, medicine_codes=self.medicine_codes)
        # check if data folder for eu_n exists and is filled
        data_folder = f"{data_path}/{self.eu_n}"
        assert path.exists(data_folder), f"data folder for {self.eu_n} does not exist"
        assert path.isdir(data_folder), f"{data_folder} is not a directory"
        assert len(os.listdir(data_folder)) > 0, f"{data_folder} is empty"
        # check if webdata is empty
        assert path.getsize(f"{data_folder}/{self.eu_n}_webdata.json") > 2, f"webdata.json is empty for {self.eu_n}"
        # check if urls.json is empty
        assert path.getsize(f"JSON/urls.json") > 2, f"urls.json is empty"

    def run_ema_scraper(self):
        web.main(data_filepath=data_path, scrape_ec=False, scrape_ema=True, download_files=False, run_filter=False,
                 use_parallelization=self.parallel, medicine_codes=self.medicine_codes)
        with open(f"JSON/urls.json") as f:
            url_dict = (json.load(f))[self.eu_n]
        assert all(x in list(url_dict.keys()) for x in ['epar_url', 'omar_url']), "ema urls not in urls.json"

    def run_download(self):
        web.main(data_filepath=data_path, scrape_ec=False, scrape_ema=False, download_files=True, run_filter=False,
                 use_parallelization=self.parallel, medicine_codes=self.medicine_codes)
        # check if filedates.json exists
        data_folder = f"{data_path}/{self.eu_n}"
        assert path.exists(f"{data_folder}/{self.eu_n}_filedates.json")
        # check if all files from urls.json are downloaded:
        with open(f"JSON/urls.json") as f:
            url_dict = (json.load(f))[self.eu_n]
        filecount = len(url_dict["aut_url"]) + len(url_dict["smpc_url"])
        if url_dict["epar_url"]:
            filecount += 1
        if url_dict["omar_url"]:
            filecount += 1
        assert len(os.listdir(data_folder)) == filecount + 2, "not all files are downloaded"
        # check filedates.json contents
        with open(f"{data_folder}/{self.eu_n}_filedates.json") as f:
            filedates_dict = json.load(f)
        for file in os.listdir(data_folder):
            if ".pdf" in file:
                assert file in filedates_dict.keys(), f"{file} does not exist in filedates.json"

    def run_filter(self):
        web.main(data_filepath=data_path, scrape_ec=False, scrape_ema=False, download_files=False, run_filter=True,
                 use_parallelization=self.parallel, medicine_codes=self.medicine_codes)
        # check if filter.txt exists
        assert path.exists("filter.txt"), "filter.txt does not exist"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(data_path)
        os.rename(f"{data_path}_old", data_path)
        os.remove('filter.txt')
