from django.test import TestCase, Client
from unittest.mock import patch
from api.views.update_cache import update_cache
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from api.models.medicine_models import Medicine


class TestUpdateCache(TestCase):
    """
    Test api.update_cache in combination with scraper_urls_view
    Test if scraper_urls_view uses cache
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
            eu_od_sponsor="eu od sponsor",
            eu_od_comp_date="2000-01-05",
        )
        self.medicine.save()

    @patch('api.views.scraper.scraper_urls_view.UrlsSerializer')
    def test_update_cache(self, urls_serializer):
        """
        Test update_cache() function in combination with scraper_urls_view

         Args:
            urls_serializer (MagicMock): The mock object for the UrlsSerializer
        """

        urls_serializer.return_value.data = []

        # Call update_cache() function from api.update_cache
        update_cache()

        self.client.get('/api/scraper/urls/')

        # Test if UrlsSerializer hasn't been called, this means cache has been used
        self.assertEqual(urls_serializer.call_args_list, [])
