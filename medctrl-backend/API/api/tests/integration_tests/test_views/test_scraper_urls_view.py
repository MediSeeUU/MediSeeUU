from django.test import TestCase, Client
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from api.scraper.scraper_urls_view import UrlsViewSet
from api.models.medicine_models import Medicine

class ScraperUrlsViewTestCase(TestCase):
    """
    Test if scraper_urls_view works correctly
    """
    def setUp(self):
        # Add all permission to anonymous group so test can view urls view
        call_command("create_column_permissions")
        call_command("init_setup")
        for permission in Permission.objects.all():
            Group.objects.get(name="anonymous").permissions.add(permission)

        # Create Django test client that will view the endpoints
        self.client = Client()

        # Add example medicine to test database
        self.medicine = Medicine(
            eu_pnumber=21,
            atc_code="C03CA01",
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

    def test_scraper_urls_view(self):
        """
        Test if scraper_urls_view works correctly
        """
        urls_response = self.client.get('/api/scraper/urls/')
        self.assertEqual(urls_response.status_code, 200)

        response_data = urls_response.json()
        expected_data = {
            "21": {
                "ema_url": "emaurl.com",
                "ec_url": "ecurl.com",
                "aut_url": "auturl.com",
                "smpc_url": "smpcurl.com",
                "epar_url": "eparurl.com",
                "omar_url": "omarurl.com",
                "odwar_url": "odwarurl.com",
            }
        }
        self.assertEqual(sorted(expected_data.items()), sorted(response_data.items()))
