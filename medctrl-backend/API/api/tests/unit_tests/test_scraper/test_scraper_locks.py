from django.test import TestCase
from unittest.mock import patch
from api.views.scraper.post.scraper_post import ScraperMedicine
from api.models.human_models import (
    MedicinalProduct,
    IngredientsAndSubstances,
    MarketingAuthorisation,
    AcceleratedAssessment,
    Duration,
    Procedures,
    OrphanProduct,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
    HistoryEUOrphanCon,
    LegalBases,
)
from api.models.other.medicine_locks import Locks
from api.models.common import (
    AutStatus,
    AutTypes,
    LegalBasesTypes,
)


class ScraperLocksTestCase(TestCase):
    """
    Test if lock works correctly when posting to the scraper post function
    """

    @patch('api.views.scraper.scraper_medicine_post.AuthorisationStatusSerializer')
    @patch('api.views.scraper.scraper_medicine_post.PrimeSerializer', is_valid=True)
    @patch('api.views.scraper.scraper_medicine_post.MedicineFlexVarUpdateSerializer', is_valid=True)
    def test_scraper_update_lock(self, update_serializer, prime_serializer, status_serializer):
        """
        Test if lock works correctly when updating an existing medicine

        Args:
            update_serializer (MagicMock): The mock object for the MedicineFlexVarUpdateSerializer
            prime_serializer (MagicMock): The mock object for the PrimeSerializer
            status_serializer (MagicMock): The mock object for the AuthorisationStatusSerializer
        """

        self.ingredients_and_substances = IngredientsAndSubstances(
            active_substance="ACTIVE SUBSTANCE",
            atc_code="C03CA01",
            eu_nas=True,
        )
        self.ingredients_and_substances.save()

        # sample data inserted into the database
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

        self.accelerated_assessment = AcceleratedAssessment(
            eu_accel_assess_g=True,
            eu_accel_assess_m=False,
        )
        self.accelerated_assessment.save()

        self.duration = Duration(
            assess_time_days_total=10,
            assess_time_days_active=5,
            assess_time_days_cstop=2,
            ec_decision_time_days=1000,
        )
        self.duration.save()

        MarketingAuthorisation.objects.create(
            eu_pnumber=self.medicine,
            ema_procedure_start_initial="2000-01-01",
            chmp_opinion_date="2000-01-02",
            eu_aut_date="2000-01-03",
            aut_url="auturl.com",
            smpc_url="smpcurl.com",
            epar_url="eparurl.com",
            ema_rapp="ema rapp",
            ema_corapp="ema corapp",
            ema_accelerated_assessment=self.accelerated_assessment,
            duration=self.duration,
            ema_reexamination=False,
        )

        Procedures.objects.create(
            eu_pnumber=self.medicine,
            eu_suspension=True,
            eu_referral=True,
        )

        self.orphan_product = OrphanProduct(
            eu_od_number="8",
            omar_url="omarurl.com",
            odwar_url="odwarurl.com",
            ema_od_number="500",
            eu_od_con="eu od con",
            eu_od_date="2000-01-04",
            eu_od_sponsor="eu od sponsor",
            eu_od_comp_date="2000-01-05",
        )
        self.orphan_product.save()

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
            eu_od_number=self.orphan_product,
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

        # test if flex update serializer is called correctly
        update_data = update_serializer.call_args.kwargs["data"]
        update_expected = {
            "eu_pnumber": "15",
            "omar_url": "https://newomarurl.com",
            "eu_prime": [
                {
                    "eu_prime": False,
                    "change_date": "2023-01-02",
                }
            ],
        }
        self.assertDictEqual(update_data, update_expected)

        # Test if prime serializer is called correctly
        prime_data = prime_serializer.call_args.args[1]
        prime_expected = {
            "eu_pnumber": "15",
            "eu_prime": False,
            "change_date": "2023-01-02",
        }
        self.assertDictEqual(prime_data, prime_expected)

        # Test if authorisation status serializer doesn't get called
        status_data = status_serializer.call_args
        self.assertIsNone(status_data)
