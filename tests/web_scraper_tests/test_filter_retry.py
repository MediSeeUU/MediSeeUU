import unittest
import tempfile
from scraping.web_scraper import filter_retry
from scraping.utilities.web import json_helper
from parameterized import parameterized
import scraping.utilities.definitions.attributes as attr
import os

data_filepath = "../test_data/active_withdrawn"
if "web_scraper_tests" in os.getcwd():
    data_filepath = "../../test_data/active_withdrawn"

class TestFilterRetry(unittest.TestCase):

    @parameterized.expand([
        [b"EU-1-00-000_o_w_dec_0.pdf@https://ec.europa.eu/health/documents/community-register/2005/2005122310805"
         b"/dec_10805_en.pdf@corrupt@EU/3/05/339@no_pdf_json_found"],
        [b"EU-3-05-339_o_w_dec_0.pdf@https://ec.europa.eu/health/documents/community-register/2005/2005122310805"
         b"/dec_10805_en.pdf@corrupt@EU/3/05/339@no_pdf_json_found"]
    ])
    def test_retry_all(self, file_content):
        """
        Args:
            file_content: The mocked content of filter.txt
        """
        url_dict = {"EU-3-05-339": {attr.ec_url: "https://ec.europa.eu/health/documents/community-register/html/o339.htm",
                                    attr.aut_url: ["https://ec.europa.eu/health/documents/community-register/2005"
                                                "/2005122310805/dec_10805_en.pdf"],
                                    attr.smpc_url: [],
                                    attr.ema_url: [
                                        "http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/orphans"
                                        "/2009/11/human_orphan_000555.jsp&murl=menus/medicines/medicines.jsp&mid"
                                        "=WC0b01ac058001d12b",
                                        "http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/medicines"
                                        "/000709/human_med_001062.jsp&murl=menus/medicines/medicines.jsp&mid"
                                        "=WC0b01ac058001d124"],
                                    attr.epar_url: "https://www.ema.europa.eu/documents/scientific-discussion/sprycel"
                                                "-epar-scientific-discussion_en.pdf",
                                    attr.omar_url: ""}}
        url_file = json_helper.JsonHelper(init_dict=url_dict, path=f"urls_download.json")
        url_refused_file = json_helper.JsonHelper(init_dict={}, path=f"refused_urls_download.json")
        # Make a temporary file and test for key error if eu number is not in the url dictionary
        temp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        temp.write(str(file_content))
        temp.seek(0)
        temp.close()
        self.assertIsNone(filter_retry.retry_medicine(temp.name, url_file, data_filepath, url_refused_file))

    @parameterized.expand([
        ["EU-1-04-273", ["h", "anx", "0"]],  # normal
        ["EU-1-04-273", ["h", "an", "0"]],  # typo in pdf_type
        ["EU-1-00-129", ["h", "dec", "0"]],  # no url available
        ["EU-3-05-339", ["o", "dec", "0"]]  # orphan, in filter.txt
    ])
    def test_retry_download(self, eu_n, filename_el):
        """
        Args:
            eu_n: The eu nummer of the tested medicine
            filename_el: The filename elements for a specific file
        """
        url_file = {'EU-1-00-129': {attr.ec_url: 'https://ec.europa.eu/health/documents/community-register/html/h129.htm',
                                    attr.aut_url: [''],
                                    attr.smpc_url: ['https://ec.europa.eu/health/documents/community-register/2000'
                                                 '/200003093513/anx_3513_en.pdf'],
                                    },
                    'EU-1-04-273': {attr.ec_url: 'https://ec.europa.eu/health/documents/community-register/html/h274.htm',
                                    attr.aut_url: ['https://ec.europa.eu/health/documents/community-register/2004'
                                                '/200404267651/dec_7651_en.pdf'],
                                    attr.smpc_url: ['https://ec.europa.eu/health/documents/community-register/2004'
                                                 '/200404267651/dec_7651_en.pdf'],
                                    },
                    'EU-3-05-339': {attr.ec_url: 'https://ec.europa.eu/health/documents/community-register/html/o339.htm',
                                    attr.aut_url: ['https://ec.europa.eu/health/documents/community-register/2005'
                                                '/2005122310805/dec_10805_en.pdf'],
                                    attr.smpc_url: [],
                                    attr.ema_url: [
                                        'http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/orphans'
                                        '/2009/11/human_orphan_000555.jsp&murl=menus/medicines/medicines.jsp&mid'
                                        '=WC0b01ac058001d12b',
                                        'http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/medicines'
                                        '/000709/human_med_001062.jsp&murl=menus/medicines/medicines.jsp&mid'
                                        '=WC0b01ac058001d124'],
                                    attr.epar_url: 'https://www.ema.europa.eu/documents/scientific-discussion/sprycel'
                                                '-epar-scientific-discussion_en.pdf',
                                    attr.omar_url: ''}
                    }
        if not any(x in ["anx", "dec", "omar", "public-assessment-report"] for x in filename_el):
            self.assertRaises(KeyError, lambda: filter_retry.retry_download(eu_n, filename_el, url_file[eu_n],
                                                                            data_filepath))
        else:
            self.assertIsNone(filter_retry.retry_download(eu_n, filename_el, url_file[eu_n], data_filepath))
