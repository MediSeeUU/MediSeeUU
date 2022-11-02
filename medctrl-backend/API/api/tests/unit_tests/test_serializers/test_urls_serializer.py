from django.test import TestCase
from api.models.medicine_models import Medicine
from api.serializers.medicine_serializers.scraper import UrlsSerializer

class UrlsSerializerTestCase(TestCase):
    def setUp(self):
        self.medicine = Medicine(
            eu_pnumber=1,
            active_substance="ACTIVE SUBSTANCE",
            eu_nas=True,
            ema_procedure_start_initial="2000-01-01",
            chmp_opinion_date="2000-01-02",
            eu_aut_date="2000-01-03",
            ema_url="emaurl.com",
            ec_url="ecurl.com",
            ema_number="1",
            eu_med_type="med",
            eu_atmp=False,
            aut_url="auturl.com",
            smpc_url="smpcurl.com",
            epar_url="eparurl.com",
            ema_number_check=True,
            ema_rapp="ema rapp",
            ema_corapp="ema corapp",
            eu_accel_assess_g=True,
            eu_accel_assess_m=False,
            assess_time_days_total=10,
            assess_time_days_active=5,
            assess_time_days_cstop=2,
            ec_decision_time_days=1000,
            ema_reexamination=False,
            eu_referral=True,
            eu_suspension=True,
            omar_url="omarurl.com",
            odwar_url="odwarurl.com",
            eu_od_number="8",
            ema_od_number="500",
            eu_od_con="eu od con",
            eu_od_date="2000-01-04",
            eu_od_pnumber="80",
            eu_od_sponsor="eu od sponsor",
            eu_od_comp_date="2000-01-05",

        )
        self.medicine.save()

    def test_urls_serializer(self):
        data = UrlsSerializer(self.medicine).data
        expected = {
            "eu_pnumber": "1",
            "ema_url": "emaurl.com",
            "ec_url": "ecurl.com",
            "aut_url": "auturl.com",
            "smpc_url": "smpcurl.com",
            "epar_url": "eparurl.com",
            "omar_url": "omarurl.com",
            "odwar_url": "odwarurl.com",
        }
        self.assertDictEqual(data, expected)

