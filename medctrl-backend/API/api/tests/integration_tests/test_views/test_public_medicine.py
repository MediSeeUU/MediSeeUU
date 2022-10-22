from django.test import TestCase, Client
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from api.models.medicine_models import (
    Medicine,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
    HistoryEUOrphanCon,
)
from api.models.medicine_models.common import (
    AutStatus,
    AutTypes,
    LegalBases
)


class PublicMedicineTestCase(TestCase):
    def setUp(self):
        # Add all permission to anonymous group so test can view medicines
        call_command("create_column_permissions")
        call_command("init_setup")
        for permission in Permission.objects.all():
            Group.objects.get(name="anonymous").permissions.add(permission)

        # Create Django test client that will view the endpoints
        self.client = Client()

        # Add example medicine to test database
        self.medicine = Medicine(
            eu_pnumber=1,
            atc_code="C03CA01",
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

        HistoryAuthorisationType.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-02",
            eu_aut_type=AutTypes.STANDARD,
        )

        HistoryAuthorisationStatus.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-03",
            eu_aut_status=AutStatus.ACTIVE,
        )

        HistoryBrandName.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-04",
            eu_brand_name="Brand Name 1",
        )

        HistoryOD.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-05",
            eu_od=True,
        )

        HistoryPrime.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-06",
            eu_prime=False,
        )

        HistoryMAH.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-07",
            eu_mah="MAH 1",
        )

        HistoryEUOrphanCon.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-08",
            eu_orphan_con="eu orphan con 1",
        )

    def test_structure_equal_medicine(self):
        """
        Tests if the output from structureData has the same keys as public medicine
        """

        # Test if structureData works correctly
        structure_response = self.client.get('/api/structureData/')
        self.assertEqual(structure_response.status_code, 200)

        # Get all data keys from structureData and put them in a single list
        structure_dict = structure_response.json()
        structure_keys = []
        for category in structure_dict:
            for column in structure_dict[category]:
                structure_keys.append(column["data-key"])
        structure_keys.sort()

        # Test if medicine works correctly
        medicine_response = self.client.get('/api/medicine/')
        self.assertEqual(medicine_response.status_code, 200)

        # Get all data keys from medicine and put them in a single list
        medicine_dict = medicine_response.json()
        medicine_keys = list(medicine_dict[0].keys())
        medicine_keys.sort()
        # Check if the data keys from structureData and medicine are the same
        self.assertEqual(structure_keys, medicine_keys)
