import logging
from unittest import TestCase, mock
from requests.exceptions import Timeout
from scraping.web_scraper import download, json_helper
from parameterized import parameterized

data_path = "../../data"


class TestDownload(TestCase):
    """
    Class that contains all the tests for scraping.webscraper.download
    """

    @parameterized.expand([["https://ec.europa.eu/health/documents/community-register/2022/20220324154987"
                            "/dec_154987_en.pdf",
                            "EU-1-21-1541",
                            ["h", "a", "anx", "0"]],
                           ["https://ec.europa.eu/health/documents/community-register/2022/20220324154987"
                            "/anx_154987_en.pdf",
                            "EU-1-21-1541",
                           ["h", "a", "dec", "0"]
                           ]])
    def test_download_pdf_from_url(self, url, eu_n, filename_elements):
        self.assertIsNone(download.download_pdf_from_url(url, eu_n, filename_elements, data_path))

    @parameterized.expand([["EU-1-21-1541",
                            "dec",
                            ["https://ec.europa.eu/health/documents/community-register/2022/20220324154987/dec_154987_en.pdf"]],
                           ["EU-1-21-1541",
                            "anx",
                            ["https://ec.europa.eu/health/documents/community-register/2022/20220324154987/anx_154987_en.pdf"]]
                           ])
    def test_download_pdfs_ec(self, eu_n, pdf_type, pdf_url):
        med_dict = (json_helper.JsonHelper(path=f"{data_path}/{eu_n}/{eu_n}_webdata.json")).load_json()
        self.assertIsNone(download.download_pdfs_ec(eu_n, pdf_type, pdf_url, med_dict, data_path))

    @parameterized.expand([["EU-1-21-1541",
                            "epar",
                            "https://www.ema.europa.eu/documents/assessment-report/dasatinib-accordpharma-epar-public"
                            "-assessment-report_en.pdf"],
                           ["EU-1-21-1541",
                            "omar",
                            ""]
                           ])
    def test_download_pdfs_ema(self, eu_n, pdf_type, pdf_url):
        med_dict = (json_helper.JsonHelper(path=f"{data_path}/{eu_n}/{eu_n}_webdata.json")).load_json()
        self.assertIsNone(download.download_pdfs_ema(eu_n, pdf_type, pdf_url, med_dict, data_path))

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
        self.assertIsNone(download.download_medicine_files(eu_n, url_dict, data_path))

