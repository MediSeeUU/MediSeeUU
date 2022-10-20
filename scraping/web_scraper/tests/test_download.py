from unittest import TestCase, mock
from requests.exceptions import Timeout
from scraping.web_scraper import download


class TestDownload(TestCase):
    def test_download_pdf_from_url(self):
        self.fail()

    def test_download_epar_from_url(self):
        self.fail()

    def test_download_pdfs(self):
        self.fail()

    def test_read_csv_files(self):
        self.fail()

    def test_run_parallel(self):
        self.fail()

    def test_download_pdf_from_url(self):
        url = 'https://ec.europa.eu/health/documents/community-register/2004/200404287648/anx_7648_en.pdf'
        with mock.patch('download.requests') as mock_requests:
            mock_requests.get.side_effect = Timeout
            with self.assertRaises(Timeout):
                download.download_pdf_from_url('h273', url, 'anx')
                mock_requests.get.assert_called_once()
