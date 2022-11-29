import unittest
import json
import regex as re
import requests
import scraping.utilities.web.web_utils as utils
from scraping.web_scraper import ec_scraper as ec
from parameterized import parameterized
import os


data_path = "../test_data"
if "test_ec_scraper" in os.getcwd():
    data_path = "../../test_data"


class TestEcScraper(unittest.TestCase):
    """
    Class that contains al the test for scraping.webscraper.ec_scraper
    """
    def test_scrape_medicines_list(self):
        """
        Checks whether the medicine codes from the EC website are retrieved, and whether they are stored in the correct
        format. This is done by making use of a regex.

        Returns:
            None: This function returns nothing.

        """
        url_list = ec.scrape_medicines_list()
        self.assertIsNotNone(url_list, msg="url list is empty")
        first_url = url_list[0][3]
        check = re.findall(r"[(ho]\d+", first_url)[0]
        self.assertEqual(check, first_url, msg="first url not in correct format")
        last_url = url_list[-1][3]
        print(last_url)
        check = re.findall(r"h*[ho]\d+", last_url)[0]
        self.assertEqual(check, last_url, msg="last url not in correct format")

    # Unit test that checks whether the correct data is retrieved for a certain medicine.
    @parameterized.expand([
        [
            "h412",
            "B03XA01",
            "epoetin alfa",
            "EU/1/07/412",
            "ACTIVE",
            "Abseamed",
            "Medice Arzneimittel P&#252;tter GmbH &amp; Co KG",
            ec.MedicineType.HUMAN_USE_ACTIVE
        ],
        [
            "h477",
            "L03AX14",
            "Histamine dihydrochloride",
            "EU/1/08/477",
            "ACTIVE",
            "Ceplene",
            "Laboratoires Delbert",
            ec.MedicineType.HUMAN_USE_ACTIVE
        ],
        [
            "o1230",
            "not applicable",
            "(2R,3R,4S,5R)-2-(6-amino-9H-purin-9-yl)-5-((((1r,3S)-3-(2-(5-(tert-butyl)-1H-benzo[d]imidazol-2-yl)ethyl)"
            "cyclobutyl)(isopropyl) amino)methyl)tetrahydrofuran-3,4-diol",
            "EU/3/13/1230",
            "ACTIVE",
            "EU/3/13/1230",
            "Voisin Consulting Life Sciences",
            ec.MedicineType.ORPHAN_ACTIVE
        ]
    ])
    def test_get_data_from_medicine_json(
            self,
            eu_num_short,
            exp_atc_code,
            exp_active_substance,
            exp_eu_number,
            exp_eu_aut_status,
            exp_eu_brand_name_current,
            exp_eu_mah_current,
            medicine_type
    ):
        """
        Based on a couple of test medicine, checks whether the attributes that are scraped from the medicine JSON are
        correct.

        Args:
            eu_num_short (str): The short identifier for a medicine.
            exp_atc_code (str): The expected ATC code for the medicine.
            exp_active_substance (str):  The expected active substance for the medicine.
            exp_eu_number (str): The expected EU product number for the medicine.
            exp_eu_aut_status (str): The expected authorization status for the medicine.
            exp_eu_brand_name_current (str): The expected brand name for the medicine.
            exp_eu_mah_current (str): The expected marketing authorization holder for the medicine.
            medicine_type (MedicineType): The type of medicine that is being scraped.

        Returns:
            None: This function returns nothing.

        """
        html_active = ec.get_ec_html(
            f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm")
        medicine_json, *_ = ec.get_ec_json_objects(html_active)
        medicine_dict, _ = ec.get_data_from_medicine_json(medicine_json, eu_num_short, medicine_type)

        self.assertEqual(medicine_dict["atc_code"], exp_atc_code, msg="atc codes are not equal")
        self.assertEqual(medicine_dict["active_substance"], exp_active_substance, msg="active substances are not equal")
        # check orphan specific attributes for orphan medicines, and human specific attributes for human medicines
        if "o" in eu_num_short:
            self.assertEqual(medicine_dict["eu_od_number"], exp_eu_number, msg="product numbers are not equal")
            self.assertEqual(medicine_dict["sponsor"], exp_eu_mah_current, msg="current mahs are not equal")
        else:
            self.assertEqual(medicine_dict["eu_pnumber"], exp_eu_number, msg="product numbers are not equal")
            self.assertEqual(medicine_dict["eu_mah_current"], exp_eu_mah_current, msg="current mahs are not equal")
        self.assertEqual(medicine_dict["eu_aut_status"], exp_eu_aut_status, msg="authorization statuses are not equal")
        self.assertEqual(medicine_dict["eu_brand_name_current"], exp_eu_brand_name_current, msg="current brand names "
                                                                                                "are not equal")

    @parameterized.expand([
        [
            "h477",
            "2008-10-07 00:00:00",
            "exceptional",
            "",
            "",
            ""
        ]
    ])
    def test_get_data_from_procedures_json(
            self,
            eu_num_short,
            exp_eu_aut_date,
            exp_aut_type_initial,
            exp_aut_type_current,
            exp_ema_number,
            exp_ema_number_certainty
    ):
        """
        Based on a couple of test medicine, checks whether the attributes that are scraped from the procedures JSON are
        correct.

        Args:
            eu_num_short (str): The short identifier for a medicine.
            exp_eu_aut_date (str): The expected authorization date for a medicine.
            exp_aut_type_initial: (str)  The expected initial authorization type for a medicine.
            exp_aut_type_current (str): The expected current authorization type for a medicine.
            exp_ema_number (str): The expected ema number for a medicine.
            exp_ema_number_certainty (str): The expected ema number certainty for a medicine.

        Returns:
            None: This function returns nothing.

        """
        html_active = ec.get_ec_html(
            f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm")
        _, procedures_json, *_ = ec.get_ec_json_objects(html_active)
        procedures_dict, *_ = ec.get_data_from_procedures_json(procedures_json, eu_num_short, data_path)
        self.assertEqual(procedures_dict["eu_aut_date"], exp_eu_aut_date, msg="authorization dates are not equal")
        self.assertEqual(procedures_dict["eu_aut_type_initial"], exp_aut_type_initial, msg="not equal")
        # assert procedures_dict["eu_aut_date"] == exp_eu_aut_date
        # assert procedures_dict["eu_aut_type_initial"] == exp_aut_type_initial
        # assert procedures_dict["eu_aut_type_current"] = exp_aut_type_current
        # assert procedures_dict["ema_number"] = exp_ema_number
        # assert procedures_dict["ema_number_certainty"] = exp_ema_number_certainty

    def test_scrape_active_withdrawn_jsons(self):
        """
        Checks whether the active and withdrawn medicine lists are not empty.

        Returns:
            None: This function returns nothing.

        """
        json_list: list[json] = ec.scrape_active_withdrawn_jsons()
        self.assertIsNotNone(json_list, msg="json list is empty")

    def test_scrape_refused_jsons(self):
        """
        Checks whether the refused medicine lists are not empty.

        Returns:
            None: This function returns nothing.
        """
        json_list: list[json] = ec.scrape_refused_jsons()
        self.assertIsNotNone(json_list, msg="json list is empty")

    @parameterized.expand([
        ["h944"],               # human use active
        ["h313"],               # human use withdrawn
        ["ho24765"],            # human use refused
        ["o1384"],              # orphan active
        ["o200"],               # orphan withdrawn
        ["ho26270"]             # orphan refused
    ])
    def test_get_ec_json_objects(self, eu_num_short):
        """
        Based on a couple of test medicine, checks whether it retrieves JSON objects from a medicine page.

        Args:
            eu_num_short (str): The short identifier for a medicine.
:
        Returns:
            None: This function returns nothing.

        """
        html_active = ec.get_ec_html(
            f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm")
        json_list: list[json] = ec.get_ec_json_objects(html_active)
        self.assertIsNotNone(json_list, msg="json list is empty")

    def test_scrape_medicine_page(self):
        """
        Checks whether the medicine page contains the expected data.

        Returns:
            None: This function returns nothing.
        """
        url = 'https://ec.europa.eu/health/documents/community-register/html/h273.htm'
        ema = ['http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/medicines/000521/human_med_000895'
               '.jsp&murl=menus/medicines/medicines.jsp&mid=WC0b01ac058001d124',
               'http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/orphans/2009/11/human_orphan_000281'
               '.jsp&murl=menus/medicines/medicines.jsp&mid=WC0b01ac058001d12b']
        decision = [
            'https://ec.europa.eu/health/documents/community-register/2004/200404287648/dec_7648_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2006/2006022811168/dec_11168_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2007/2007042623649/dec_23649_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2009/2009032555652/dec_55652_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2011/20111003110571/dec_110571_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2012/20120823124192/dec_124192_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2014/20140603128801/dec_128801_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2015/20150226130899/dec_130899_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2017/20170516137848/dec_137848_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2019/20190919146015/dec_146015_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2021/20210322150898/dec_150898_en.pdf'
        ]
        annex = [
            'https://ec.europa.eu/health/documents/community-register/2004/200404287648/anx_7648_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2006/2006022811168/anx_11168_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2007/2007042623649/anx_23649_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2009/2009032555652/anx_55652_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2011/20111003110571/anx_110571_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2012/20120823124192/anx_124192_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2014/20140603128801/anx_128801_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2015/20150226130899/anx_130899_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2017/20170516137848/anx_137848_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2019/20190919146015/anx_146015_en.pdf',
            'https://ec.europa.eu/health/documents/community-register/2021/20210322150898/anx_150898_en.pdf'
        ]
        html_active: requests.Response = utils.get_html_object(url)
        dec_result, anx_result, ema_result, _ = ec.scrape_medicine_page(url, html_active,
                                                                        ec.MedicineType.HUMAN_USE_ACTIVE, data_path)
        dec_result = [x[0] for x in dec_result]
        anx_result = [x[0] for x in anx_result]

        self.assertEqual(ema, ema_result, "incorrect EMA result")
        self.assertEqual(decision, dec_result, "incorrect decision result")
        self.assertEqual(annex, anx_result, "incorrect annex result")

    @parameterized.expand(
        [
            [
                [],
                "standard"
            ],
            [
                ["Annual Renewal"],
                "conditional"
            ],
            [
                ["Annual Reassessment"],
                "exceptional"
            ],
            [
                ["something else",
                 "bla bla"],
                "standard"
            ]
        ]
    )
    def test_determine_current_aut_type(self, last_decision_types, exp_output):
        """
        Tests whether the logic for determining the current authorization type is correct.

        Args:
            last_decision_types (list[str]): String for the last decision types.
            exp_output: Expected output for the function.

        Returns:
            None: This function returns nothing.

        """
        output = ec.determine_current_aut_type(last_decision_types)
        self.assertEqual(output, exp_output, msg="decision type is wrong")

    @parameterized.expand([
        [
            2005,
            True,
            False,
            "pre_2006"
        ],
        [
            2007,
            False,
            False,
            "standard"
        ],
        [
            2008,
            True,
            False,
            "exceptional"
        ],
        [
            2009,
            False,
            True,
            "conditional"
        ],
        [
            2010,
            True,
            True,
            "exceptional_conditional"
        ]
    ])
    def test_determine_initial_aut_type(self, year, is_exceptional, is_conditional, exp_output):
        output = ec.determine_initial_aut_type(year, is_exceptional, is_conditional)
        self.assertEqual(output, exp_output, msg="output is not as expected")

    @parameterized.expand([
        [
            "EMEA/H/C/000674/IA/0142/G",
            ["EMEA/H/C/000674"]
        ],
        [
            "EMA/OD/020/02",
            ["EMA/OD/020/02"]
        ],
        [
            "EMEA/H/C/000674/IA/0142/G, EMA/OD/020/02",
            [
                "EMEA/H/C/000674",
                "EMA/OD/020/02"
            ]
        ]
    ])
    def test_format_ema_number(self, ema_number, exp_output):
        """
        Tests whether EMA numbers are formatted correctly.

        Args:
            ema_number: EMA number to be formatted.
            exp_output: The expected output, how the EMA number should be formatted.

        Returns:
            None: This function returns nothing.
        """
        output = ec.format_ema_number(ema_number)
        self.assertEqual(output, exp_output, msg="output is not as expected")

    @parameterized.expand([
        [
            [
                "EMEA/H/C/000572",
                "EMEA/H/C/000572",
                "EMEA/H/C/572",
                "EMEA/H/C/IG1126",
                "EMEA/H/C/572",
                "EMEA/H/C/IG1055",
                "EMEA/H/C/572",
                "EMEA/H/C/572",
                "EMEA/H/C/572",
                "EMEA/H/C/572",
                "EMEA/H/C/572",
                "EMEA/H/C/572",
                "EMEA/H/C/572",
                "EMEA/H/C/572",
                "EMEA/H/C/572"
            ],
            "EMEA/H/C/572",
            0.75
        ]
    ])
    def test_determine_ema_number(self, ema_numbers, exp_ema_number, exp_fraction):
        """
        Tests whether the correct EMA number is chosen from a list of EMA numbers. Also checks whether the EMA number
        certainty is correct.

        Args:
            ema_numbers: List of EMA numbers to check.
            exp_ema_number: Expected EMA number.
            exp_fraction: Expected EMA number certainty.

        Returns:
            None: This function returns nothing.
        """
        ema_number, fraction = ec.determine_ema_number(ema_numbers)
        self.assertEqual(ema_number, exp_ema_number, msg="ema number is not right")
        self.assertEqual(fraction, exp_fraction, msg="fraction is not right")
