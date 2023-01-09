from os import path, remove
import os
from datetime import datetime, date
import regex as re
import json
from unittest import TestCase
from scraping.web_scraper import download
from scraping.utilities.web import json_helper
from parameterized import parameterized
import scraping.utilities.definitions.attributes as attr

data_path = "../tests/test_data"
if "web_scraper_tests" in os.getcwd():
    data_path = "../../tests/test_data"
data_local = f"{data_path}/active_withdrawn"


class TestDownload(TestCase):
    """
    Class that contains all the tests for scraping.webscraper.download
    """
    @parameterized.expand([["https://ec.europa.eu/health/documents/community-register/2000/200010185296/"
                            "dec_5296_en.pdf"],
                           ["https://www.ema.europa.eu/documents/orphan-maintenance-report/mylotarg-orphan"
                            "-maintenance-assessment-report-initial-authorisation_en.pdf"]])
    def test_get_date_from_url(self, url):
        """
        Args:
            url: url of a file that needs to be tested
        """
        filedates_dict = download.get_date_from_url(url)
        url_out = filedates_dict[attr.file_date_pdf_link]
        date1 = filedates_dict[attr.file_date_pdf_date]
        date1 = datetime.strptime(date1.split()[0], '%Y-%m-%d').date()
        date2 = filedates_dict[attr.file_date_pdf_scrape_date]
        date2 = datetime.strptime(date2.split()[0], '%Y-%m-%d').date()

        self.assertTrue(url == url_out)
        if len((re.findall(r"\d{8}", url))) > 0:
            self.assertTrue(date1 != date.today())
        self.assertTrue(date2 == date.today())

    @parameterized.expand([["https://ec.europa.eu/health/documents/community-register/2022/20220324154987"
                            "/dec_154987_en.pdf",
                            "EU-1-21-1541",
                            ["h", "anx", "0"]],
                           ["https://ec.europa.eu/health/documents/community-register/2022/20220324154987"
                            "/anx_154987_en.pdf",
                            "EU-1-21-1541",
                            ["h", "dec", "0"]]])
    def test_download_pdf_from_url(self, url, eu_n, filename_elements):
        """
        Args:
            url: The url that needs to be downloaded
            eu_n: The eu number of the file that needs to be downloaded
            filename_elements: The filename elements
        """
        target_path = f"{data_local}/{eu_n}"
        with open(f"{target_path}/{eu_n}_webdata.json") as f:
            attr_dict = json.load(f)
        self.assertIsNotNone(attr_dict)
        self.assertNotEqual({}, attr_dict)
        self.assertIsNone(download.download_pdf_from_url(url, eu_n, filename_elements, target_path, attr_dict, True))

    @parameterized.expand([["EU-1-21-1541",
                            "dec",
                            [
                                "https://ec.europa.eu/health/documents/community-register/2022/20220324154987"
                                "/dec_154987_en.pdf"]],
                           ["EU-1-21-1541",
                            "anx",
                            [
                                "https://ec.europa.eu/health/documents/community-register/2022/20220324154987"
                                "/anx_154987_en.pdf"]]
                           ])
    def test_download_pdfs_ec(self, eu_n, pdf_type, pdf_url):
        """
        Args:
            eu_n: The eu nummer of the tested medicine
            pdf_type: The type of the pdf, dec or anx
            pdf_url: The url of the pdf
        """
        assert path.exists(f"{data_local}/{eu_n}/{eu_n}_webdata.json"), \
            f"can't run test, no webdata file for {eu_n}"
        med_dict = (json_helper.JsonHelper(path=f"{data_local}/{eu_n}/{eu_n}_webdata.json")).load_json()
        url_json: json_helper.JsonHelper = json_helper.JsonHelper(path="test_json.json", init_dict={})
        target_path = f"{data_local}/{eu_n}"
        self.assertIsNone(download.download_pdfs_ec(eu_n, pdf_type, pdf_url, med_dict, target_path, url_json, True))
        remove("test_json.json")

    @parameterized.expand([["EU-1-21-1541",
                            "epar",
                            "https://www.ema.europa.eu/documents/assessment-report/dasatinib-accordpharma-epar-public"
                            "-assessment-report_en.pdf"],
                           ["EU-1-21-1541",
                            "omar",
                            ""]
                           ])
    def test_download_pdfs_ema(self, eu_n, pdf_type, pdf_url):
        """
        Args:
            eu_n: The eu nummer of the tested medicine
            pdf_type: The type of pdf, epar or omar
            pdf_url: The url of the pdf
        """
        assert path.exists(f"{data_local}/{eu_n}/{eu_n}_webdata.json"), \
            f"can't run test, no webdata file for {eu_n}"
        med_dict = (json_helper.JsonHelper(path=f"{data_local}/{eu_n}/{eu_n}_webdata.json")).load_json()
        target_path = f"{data_local}/{eu_n}"
        self.assertIsNone(download.download_pdfs_ema(eu_n, pdf_type, pdf_url, med_dict, target_path, True))

    @parameterized.expand([["EU-1-21-1541",
                            {attr.ec_url: "https://ec.europa.eu/health/documents/community-register/html/h1541.htm",
                             attr.aut_url: ["https://ec.europa.eu/health/documents/community-register/2022/20220324154987"
                                         "/dec_154987_en.pdf"],
                             attr.smpc_url: ["https://ec.europa.eu/health/documents/community-register/2022"
                                          "/20220324154987/anx_154987_en.pdf"],
                             attr.ema_url: ["https://www.ema.europa.eu/en/medicines/human/EPAR/dasatinib-accordpharma"],
                             attr.epar_url: "https://www.ema.europa.eu/documents/assessment-report/dasatinib-accordpharma"
                                         "-epar-public-assessment-report_en.pdf",
                             attr.omar_url: "",
                             attr.odwar_url: "",
                             attr.other_ema_urls: []}
                            ]])
    def test_download_medicine_files(self, eu_n, url_dict):
        """
        Args:
            eu_n: The eu number of the tested medicine
            url_dict: The dictionary containing the urls for a specific medicine
        """
        url_json: json_helper.JsonHelper = json_helper.JsonHelper(path="urls.json", init_dict=url_dict)
        assert path.exists(f"{data_local}/{eu_n}/{eu_n}_webdata.json"), \
            f"can't run test, no webdata file for {eu_n}"
        self.assertIsNone(download.download_medicine_files(eu_n, url_dict, url_json, data_path))
        remove("urls.json")
