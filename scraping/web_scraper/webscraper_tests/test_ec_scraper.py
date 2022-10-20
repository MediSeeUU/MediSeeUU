from unittest import TestCase, mock
import sys
import regex as re
from ...src import ec_scraper


class TestEcScraper(TestCase):
    def test_scrape_medicine_list(self):
        url_list = ec_scraper.scrape_medicines_list("https://ec.europa.eu/health/documents/community-register/html/reg_hum_act.htm")
        self.assertIsNotNone(url_list, msg="url list is empty")
        first_url = url_list[0]
        check = re.findall(r"h\d+", first_url)[0]
        self.assertEqual(check, first_url, msg="first url not in correct format")
        last_url = url_list[-1]
        check = re.findall(r"h\d+", last_url)[0]
        self.assertEqual(check, last_url, msg="last url not in correct format")

    # NOTE: only tests one case.
    def test_scrape_medicine_page(self):
        url = 'h273'
        ema = ['http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/medicines/000521/human_med_000895'
               '.jsp&murl=menus/medicines/medicines.jsp&mid=WC0b01ac058001d124',
               'http://www.ema.europa.eu/ema/index.jsp?curl=pages/medicines/human/orphans/2009/11/human_orphan_000281'
               '.jsp&murl=menus/medicines/medicines.jsp&mid=WC0b01ac058001d12b']
        decision = ['https://ec.europa.eu/health/documents/community-register/2004/200404287648/dec_7648_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2006/2006022811168/dec_11168_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2007/2007042623649/dec_23649_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2009/2009032555652/dec_55652_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2011/20111003110571/dec_110571_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2012/20120823124192/dec_124192_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2014/20140603128801/dec_128801_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2015/20150226130899/dec_130899_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2017/20170516137848/dec_137848_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2019/20190919146015/dec_146015_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2021/20210322150898/dec_150898_en.pdf']
        annex = ['https://ec.europa.eu/health/documents/community-register/2004/200404287648/anx_7648_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2006/2006022811168/anx_11168_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2007/2007042623649/anx_23649_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2009/2009032555652/anx_55652_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2011/20111003110571/anx_110571_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2012/20120823124192/anx_124192_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2014/20140603128801/anx_128801_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2015/20150226130899/anx_130899_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2017/20170516137848/anx_137848_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2019/20190919146015/anx_146015_en.pdf', 'https://ec.europa.eu/health/documents/community-register/2021/20210322150898/anx_150898_en.pdf']
        dec_result, anx_result, ema_result = ec_scraper.scrape_medicine_page(url)
        self.assertEqual(ema, ema_result, "incorrect EMA result")
        self.assertEqual(decision, dec_result, "incorrect decision result")
        self.assertEqual(annex, anx_result, "incorrect annex result")




