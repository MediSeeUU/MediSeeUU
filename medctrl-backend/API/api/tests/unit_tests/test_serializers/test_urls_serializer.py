from django.test import TestCase
from api.models.medicine_models import (
    MedicinalProduct,
    IngredientsAndSubstances,
)
from api.serializers.medicine_serializers.scraper import UrlsSerializer


class UrlsSerializerTestCase(TestCase):
    def setUp(self):
        self.ingredients_and_substances = IngredientsAndSubstances(
            active_substance="ACTIVE SUBSTANCE",
            atc_code="C03CA01",
            eu_nas=True,
        )
        self.ingredients_and_substances.save()

        self.medicine = MedicinalProduct(
            eu_pnumber="15",
            ema_url="emaurl.com",
            ec_url="ecurl.com",
            ema_number="1",
            eu_med_type="med",
            eu_atmp=False,
            ema_number_check=True,
            ingredients_and_substances=self.ingredients_and_substances,
        )
        self.medicine.save()

    def test_urls_serializer(self):
        data = UrlsSerializer(self.medicine).data
        expected = {
            "eu_pnumber": "15",
            "ema_url": "emaurl.com",
            "ec_url": "ecurl.com",
        }
        self.assertDictEqual(data, expected)

