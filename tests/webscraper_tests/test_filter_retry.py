import unittest
import tempfile
from scraping.web_scraper import filter_retry, json_helper
from unittest.mock import patch, mock_open, MagicMock
from parameterized import parameterized


data_filepath = "../../data"


class TestFilterRetry(unittest.TestCase):

    @parameterized.expand([
        [b"EU-1-00-000_o_w_dec_0.pdf@https://ec.europa.eu/health/documents/community-register/2005/2005122310805"
         b"/dec_10805_en.pdf@corrupt@EU/3/05/339@no_pdf_json_found"],
        [b"EU-3-05-339_o_w_dec_0.pdf@https://ec.europa.eu/health/documents/community-register/2005/2005122310805"
         b"/dec_10805_en.pdf@corrupt@EU/3/05/339@no_pdf_json_found"]
    ])
    def test_retry_all(self, file_content):
        url_file = {"EU-3-05-339": {"ec_url": "https://ec.europa.eu/health/documents/community-register/html/o339.htm",
                                    "aut_url": ["https://ec.europa.eu/health/documents/community-register/2005"
                                                "/2005122310805/dec_10805_en.pdf"],
                                    "smpc_url": [],
                                    "ema_url": [
                                        "http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/orphans"
                                        "/2009/11/human_orphan_000555.jsp&murl=menus/medicines/medicines.jsp&mid"
                                        "=WC0b01ac058001d12b",
                                        "http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/medicines"
                                        "/000709/human_med_001062.jsp&murl=menus/medicines/medicines.jsp&mid"
                                        "=WC0b01ac058001d124"],
                                    "epar_url": "https://www.ema.europa.eu/documents/scientific-discussion/sprycel"
                                                "-epar-scientific-discussion_en.pdf",
                                    "omar_url": ""}}
        # Make a temporary file and test for key error if eu number is not in the url dictionary
        temp = tempfile.TemporaryFile()
        temp.write(file_content)
        temp.seek(0)
        self.assertIsNone(filter_retry.retry_all(temp.name, url_file))

    @parameterized.expand([
        ["EU-1-04-273", ["h", "a", "anx", "0"]], # normal
        ["EU-1-04-273", ["h", "a", "an", "0"]], # typo in pdf_type
        ["EU-1-00-129", ["h", "a", "dec", "0"]], # no url available
        ["EU-3-05-339", ["o", "w", "dec", "0"]] # orphan, in filter.txt
    ])
    def test_retry_download(self, eu_n, filename_el):
        url_file = {'EU-1-00-129': {'ec_url': 'https://ec.europa.eu/health/documents/community-register/html/h129.htm',
                                    'aut_url': [''],
                                    'smpc_url': ['https://ec.europa.eu/health/documents/community-register/2000'
                                                 '/200003093513/anx_3513_en.pdf'],
                                    },
                    'EU-1-04-273': {'ec_url': 'https://ec.europa.eu/health/documents/community-register/html/h274.htm',
                                    'aut_url': ['https://ec.europa.eu/health/documents/community-register/2004'
                                                '/200404267651/dec_7651_en.pdf'],
                                    'smpc_url': ['https://ec.europa.eu/health/documents/community-register/2004'
                                                 '/200404267651/dec_7651_en.pdf'],
                                    },
                    'EU-3-05-339': {'ec_url': 'https://ec.europa.eu/health/documents/community-register/html/o339.htm',
                                    'aut_url': ['https://ec.europa.eu/health/documents/community-register/2005'
                                                '/2005122310805/dec_10805_en.pdf'],
                                    'smpc_url': [],
                                    'ema_url': [
                                        'http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/orphans'
                                        '/2009/11/human_orphan_000555.jsp&murl=menus/medicines/medicines.jsp&mid'
                                        '=WC0b01ac058001d12b',
                                        'http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/medicines'
                                        '/000709/human_med_001062.jsp&murl=menus/medicines/medicines.jsp&mid'
                                        '=WC0b01ac058001d124'],
                                    'epar_url': 'https://www.ema.europa.eu/documents/scientific-discussion/sprycel'
                                                '-epar-scientific-discussion_en.pdf',
                                    'omar_url': ''}
                    }
        if not any(x in ["anx", "dec", "omar", "public-assessment-report"] for x in filename_el):
            self.assertRaises(KeyError, lambda: filter_retry.retry_download(eu_n, filename_el, url_file[eu_n],
                                                                            data_filepath))
        else:
            self.assertIsNone(filter_retry.retry_download(eu_n, filename_el, url_file[eu_n], data_filepath))
