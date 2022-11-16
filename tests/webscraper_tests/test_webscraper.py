import os.path as path
import os
import shutil
from unittest import TestCase
from scraping.web_scraper import __main__ as web
from parameterized import parameterized
data_path = "../../data"
if not path.isdir(data_path):
    os.mkdir(data_path)


class TestWebScraper(TestCase):
    """
    Class that runs web
    """

    @parameterized.expand([[True, [('https://ec.europa.eu/health/documents/community-register/html/h273.htm',
                                   'EU-1-04-273', 0, 'h273')]],
                           [False, [('https://ec.europa.eu/health/documents/community-register/html/h273.htm',
                                    'EU-1-04-273', 0, 'h273')]]])
    def test_run_web(self, parallel, medicine_codes):
        os.rename(data_path, f"{data_path}_old")
        os.mkdir(data_path)
        # TODO: do the same renaming/deleting thing for urls.json file
        self.parallel = parallel
        self.medicine_codes = medicine_codes
        web.main(data_filepath=data_path, scrape_ec=True, scrape_ema=False, download_files=False, run_filter=False,
                 use_parallelization=self.parallel, medicine_codes=self.medicine_codes)

        web.main(data_filepath=data_path, scrape_ec=False, scrape_ema=True, download_files=False, run_filter=False,
                 use_parallelization=self.parallel, medicine_codes=self.medicine_codes)

        web.main(data_filepath=data_path, scrape_ec=False, scrape_ema=False, download_files=True, run_filter=False,
                 use_parallelization=self.parallel, medicine_codes=self.medicine_codes)

        web.main(data_filepath=data_path, scrape_ec=False, scrape_ema=False, download_files=False, run_filter=True,
                 use_parallelization=self.parallel, medicine_codes=self.medicine_codes)
        shutil.rmtree(data_path)
        os.rename(f"{data_path}_old", data_path)

    @parameterized.expand([[True, [('https://ec.europa.eu/health/documents/community-register/html/h273.htm',
                                   'EU-1-04-273', 0, 'h273')]],
                           [False, [('https://ec.europa.eu/health/documents/community-register/html/h273.htm',
                                    'EU-1-04-273', 0, 'h273')]]])
    def test_run_web2(self, parallel, medicine_codes):
        os.rename(data_path, f"{data_path}_old")
        os.mkdir(data_path)
        # TODO: do the same renaming/deleting thing for urls.json file
        self.parallel = parallel
        self.medicine_codes = medicine_codes
        web.main(data_filepath=data_path, scrape_ec=True, scrape_ema=True, download_files=True, run_filter=True,
                 use_parallelization=self.parallel, medicine_codes=self.medicine_codes)
        shutil.rmtree(data_path)
        os.rename(f"{data_path}_old", data_path)


