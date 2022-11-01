from django.test import TestCase
from api.scraper.scraper_medicine import ScraperMedicine
from api.models.medicine_models import (
    Medicine,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
    HistoryEUOrphanCon,
    LegalBases,
)
from api.models.other.locks import Locks
from api.serializers.medicine_serializers.scraper import (
    MedicineSerializer,
    AuthorisationStatusSerializer,
    PrimeSerializer,
)
from api.models.medicine_models.common import (
    AutStatus,
    AutTypes,
    LegalBasesTypes,
)

class ScraperLocksTestCase(TestCase):
    """
    Test if lock works correctly when posting to the scraper post function
    """
    def test_scraper_update_lock(self):
        """
        Test if lock works correctly when updating an existing medicine
        """

        # sample data inserted into the database
        self.medicine = Medicine(
            eu_pnumber=15,
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
            eu_prime=True,
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
        LegalBases.objects.create(
            eu_pnumber=self.medicine,
            eu_legal_basis=LegalBasesTypes.article10_a,
        )

        Locks.objects.create(
            eu_pnumber=self.medicine,
            column_name="ema_url",
        )
        Locks.objects.create(
            eu_pnumber=self.medicine,
            column_name="eu_aut_status",
        )

        # data to be updated by the scraper post endpoint
        self.data = {
            "override": False,
            "data": [
                {
                    "eu_pnumber": "15",
                    "ema_url": "https://newemaurl.com",
                    "omar_url": "https://newomarurl.com",

                    "eu_aut_status": [
                        {
                            "eu_aut_status": "WITHDRAWN",
                            "change_date": "2023-01-01",
                        }
                    ],
                    "eu_prime": [
                        {
                            "eu_prime": False,
                            "change_date": "2023-01-02",
                        }
                    ],
                }
            ]
        }
        scraper = ScraperMedicine()
        scraper.post(self)

        medicine_query = Medicine.objects.first()
        medicine_data = dict(MedicineSerializer(medicine_query).data)

        # ema_url is locked, so test it hasn't updated
        self.assertEqual(medicine_data["ema_url"], "emaurl.com")

        # omar_url isn't locked, so test it has updated
        self.assertEqual(medicine_data["omar_url"], "https://newomarurl.com")


        # test if locked eu_aut_status history object hasn't been inserted
        eu_aut_status_query = HistoryAuthorisationStatus.objects.order_by('change_date').last()
        eu_aut_status_data = AuthorisationStatusSerializer(eu_aut_status_query).data
        eu_aut_status_expected = {
            "eu_pnumber": "15",
            "eu_aut_status": "ACTIVE",
            "change_date": "2022-01-03",
        }
        self.assertEqual(sorted(dict(eu_aut_status_data).items()), sorted(eu_aut_status_expected.items()))

        # test if new eu_prime history object has been inserted
        eu_prime_query = HistoryPrime.objects.order_by('change_date').last()
        eu_prime_data = PrimeSerializer(eu_prime_query).data
        eu_prime_expected = {
            "eu_pnumber": "15",
            "eu_prime": False,
            "change_date": "2023-01-02",
        }
        self.assertEqual(sorted(dict(eu_prime_data).items()), sorted(eu_prime_expected.items()))
