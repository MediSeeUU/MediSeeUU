from unittest import TestCase, mock
import sys
import pytest
import regex as re
from scraping.web_scraper import ec_scraper as ec


class TestEcScraper(TestCase):
    """
    Class that contains al the test for scraping.webscraper.ec_scraper
    """
    def test_scrape_medicines_list(self):
        url_list = ec.scrape_medicines_list()
        self.assertIsNotNone(url_list, msg="url list is empty")
        first_url = url_list[0][3]
        check = re.findall(r"[ho]\d+", first_url)[0]
        self.assertEqual(check, first_url, msg="first url not in correct format")
        last_url = url_list[-1][3]
        check = re.findall(r"[ho]\d+", last_url)[0]
        self.assertEqual(check, last_url, msg="last url not in correct format")

    def test_scrape_active_withdrawn_jsons(self):
        self.fail()

    def test_scrape_refused_jsons(self):
        self.fail()

    def test_get_ec_json_objects(self):
        self.fail()

    def test_scrape_medicine_page(self):
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
        dec_result, anx_result, ema_result, _ = ec.scrape_medicine_page(url, ec.MedicineType.HUMAN_USE_ACTIVE)
        self.assertEqual(ema, ema_result, "incorrect EMA result")
        self.assertEqual(decision, dec_result, "incorrect decision result")
        self.assertEqual(annex, anx_result, "incorrect annex result")

    # Unit test that checks whether the correct data is retrieved for a certain medicine.
    @pytest.mark.parametrize(
        "eu_num_short, "
        "exp_atc_code, "
        "exp_active_substance, "
        "exp_eu_pnumber, "
        "exp_eu_aut_status, "
        "exp_eu_brand_name_current, "
        "exp_eu_mah_current",
        [
            ("h412",
             "B03XA01",
             "epoetin alfa",
             "EU/1/07/412",
             "ACTIVE",
             "Abseamed",
             "Medice Arzneimittel P&#252;tter GmbH &amp; Co KG"
             ),
            ("h477",
             "L03AX14",
             "Histamine dihydrochloride",
             "EU/1/08/477",
             "ACTIVE",
             "Ceplene",
             "Laboratoires Delbert"
             ),
            ("o1230",
             None,
             "(2R,3R,4S,5R)-2-(6-amino-9H-purin-9-yl)-5-((((1r,3S)-3-(2-(5-(tert-butyl)-1H-benzo[d]imidazol-2-yl)ethyl)cyclobutyl)(isopropyl) amino)methyl)tetrahydrofuran-3,4-diol",
             "EU/3/13/1230",
             "ACTIVE",
             "EU/3/13/1230",
             "Voisin Consulting Life Sciences"
             )
        ]
    )
    def test_get_data_from_medicine_json(
            eu_num_short,
            exp_atc_code,
            exp_active_substance,
            exp_eu_pnumber,
            exp_eu_aut_status,
            exp_eu_brand_name_current,
            exp_eu_mah_current
    ):
        html_active = ec.get_ec_html(
            f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm")
        medicine_json, *_ = ec.get_ec_json_objects(html_active)
        medicine_dict, _ = ec.get_data_from_medicine_json(medicine_json)

        assert medicine_dict["atc_code"] == exp_atc_code
        assert medicine_dict["active_substance"] == exp_active_substance
        assert medicine_dict["eu_pnumber"] == exp_eu_pnumber
        assert medicine_dict["eu_aut_status"] == exp_eu_aut_status
        assert medicine_dict["eu_brand_name_current"] == exp_eu_brand_name_current
        assert medicine_dict["eu_mah_current"] == exp_eu_mah_current

    @pytest.mark.parametrize(
        "eu_num_short, "
        "exp_eu_aut_date, "
        "exp_aut_type_initial, "
        "exp_aut_type_current, "
        "exp_ema_number, "
        "exp_ema_number_certainty",
        [
            (
                    "h477",
                    "07-10-2008",
                    "exceptional",
                    "",
                    "",
                    ""
            )
        ]
    )
    def test_get_data_from_procedures_json(
            eu_num_short,
            exp_eu_aut_date,
            exp_aut_type_initial,
            exp_aut_type_current,
            exp_ema_number,
            exp_ema_number_certainty
    ):
        html_active = ec.get_ec_html(
            f"https://ec.europa.eu/health/documents/community-register/html/{eu_num_short}.htm")
        _, procedures_json, *_ = ec.get_ec_json_objects(html_active)
        procedures_dict, *_ = ec.get_data_from_procedures_json(procedures_json)

        assert procedures_dict["eu_aut_date"] == exp_eu_aut_date
        assert procedures_dict["eu_aut_type_initial"] == exp_aut_type_initial
        # assert procedures_dict["eu_aut_type_current"] = exp_aut_type_current
        # assert procedures_dict["ema_number"] = exp_ema_number
        # assert procedures_dict["ema_number_certainty"] = exp_ema_number_certainty

    def test_determine_current_aut_type(self):
        self.fail()

    def test_determine_aut_type(self):
        self.fail()

    def test_format_ema_number(self):
        self.fail()

    def test_determine_ema_number(self):
        self.fail()