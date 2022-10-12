from django.test import TestCase
from api.serializers.medicine_serializers.public_medicine import PublicMedicineSerializer

class PublicMedicineSerializerTestCase(TestCase)
    def setUp(self):
        self.atc_code = {
            'eu_pnumber': "1",
            'change_date': "01/01/2022",
            'atc_code': "C03CA01",
        }
        self.eu_aut_type_history = {
            'eu_pnumber': "1",
            'change_date': "01/01/2022",
            'eu_aut_type': "12345678910",
        }
        self.eu_aut_status_history = {
            'eu_pnumber': "1",
            'change_date': "01/01/2022",
            'eu_aut_status': "ACTIVE",
        }
        self.eu_brand_name_history = {
            'eu_pnumber': "1",
            'change_date': "01/01/2022",
            'eu_brand_name': "Brand Name",
        }
        self.eu_orphan_history = {
            'eu_pnumber': "1",
            'change_date': "01/01/2022",
            'eu_od': "True",
        }
        self.eu_prime_history = {
            'eu_pnumber': "1",
            'change_date': "01/01/2022",
            'eu_prime': "False",
        }
        self.eu_mah_history = {
            'eu_pnumber': "1",
            'change_date': "01/01/2022",
            'eu_mah': "MAH",
        }
        self.ema_number_check_history = {
            'eu_pnumber': "1",
            'change_date': "01/01/2022",
            'ema_number_check': "True",
        }

    def test_public_medicine_serializer(self):
        pass
