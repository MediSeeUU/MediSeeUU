import logging
from os import path, remove
from datetime import datetime
import regex as re
from unittest import TestCase, mock
from requests.exceptions import Timeout
from scraping.web_scraper import download, json_helper
from parameterized import parameterized

data_path = "../../data"


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
        (url_out, date1, date2) = download.get_date_from_url(url)
        self.assertTrue(url == url_out)
        if len((re.findall(r"\d{8}", url))) > 0:
            self.assertTrue(date1.date() != datetime.now().date())
        self.assertTrue(date2.date() == datetime.now().date())


    @parameterized.expand([["https://ec.europa.eu/health/documents/community-register/2022/20220324154987"
                            "/dec_154987_en.pdf",
                            "EU-1-21-1541",
                            ["h", "a", "anx", "0"]],
                           ["https://ec.europa.eu/health/documents/community-register/2022/20220324154987"
                            "/anx_154987_en.pdf",
                            "EU-1-21-1541",
                            ["h", "a", "dec", "0"]]])
    def test_download_pdf_from_url(self, url, eu_n, filename_elements):
        """
        Args:
            url: The url that needs to be downloaded
            eu_n: The eu number of the file that needs to be downlaoded
            filename_elements: The filename elements
        """
        self.assertIsNone(download.download_pdf_from_url(url, eu_n, filename_elements, data_path, {}, overwrite=True))

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
        assert path.exists(f"{data_path}/{eu_n}/{eu_n}_webdata.json"), f"can't run test, no webdata file for {eu_n}"
        med_dict = (json_helper.JsonHelper(path=f"{data_path}/{eu_n}/{eu_n}_webdata.json")).load_json()
        url_json: json_helper.JsonHelper = json_helper.JsonHelper(path="test_json.json", init_dict={})
        self.assertIsNone(download.download_pdfs_ec(eu_n, pdf_type, pdf_url, med_dict, {}, data_path, url_json, True))
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
        assert path.exists(f"{data_path}/{eu_n}/{eu_n}_webdata.json"), f"can't run test, no webdata file for {eu_n}"
        med_dict = (json_helper.JsonHelper(path=f"{data_path}/{eu_n}/{eu_n}_webdata.json")).load_json()
        self.assertIsNone(download.download_pdfs_ema(eu_n, pdf_type, pdf_url, med_dict, {}, data_path))

    @parameterized.expand([["EU-1-21-1541",
                            {"ec_url": "https://ec.europa.eu/health/documents/community-register/html/h1541.htm",
                             "aut_url": ["https://ec.europa.eu/health/documents/community-register/2022/20220324154987"
                                         "/dec_154987_en.pdf"],
                             "smpc_url": ["https://ec.europa.eu/health/documents/community-register/2022"
                                          "/20220324154987/anx_154987_en.pdf"],
                             "ema_url": ["https://www.ema.europa.eu/en/medicines/human/EPAR/dasatinib-accordpharma"],
                             "epar_url": "https://www.ema.europa.eu/documents/assessment-report/dasatinib-accordpharma"
                                         "-epar-public-assessment-report_en.pdf",
                             "omar_url": ""}
                            ]])
    def test_download_medicine_files(self, eu_n, url_dict):
        """
        Args:
            eu_n: The eu number of the tested medicine
            url_dict: The dictionary containing the urls for a specific medicine
        """
        url_json: json_helper.JsonHelper = json_helper.JsonHelper(path="urls.json", init_dict=url_dict)
        assert path.exists(f"{data_path}/{eu_n}/{eu_n}_webdata.json"), f"can't run test, no webdata file for {eu_n}"
        self.assertIsNone(download.download_medicine_files(eu_n, url_dict, url_json, data_path))
        remove("urls.json")
