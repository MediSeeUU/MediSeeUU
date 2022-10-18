from django.test import TestCase
from api.models.medicine_models import Medicine
from api.models.medicine_models.common import LegalBases
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
            eu_legal_basis=LegalBases.article10_a,
            ema_url="emaurl.com",
            ec_url="ecurl.com",
            ema_number="1",
            eu_med_type="med",
            eu_atmp=False,
            aut_url="auturl.com",
            smpc_url="smpcurl.com",
            epar_url="eparurl.com",
            ema_number_check=True
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
        }
        self.assertEqual(data, expected)

