from django.test import TestCase
from unittest.mock import patch
from api.scraper.scraper_medicine_post import ScraperMedicine
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
from api.models.medicine_models.common import (
    AutStatus,
    AutTypes,
    LegalBasesTypes,
)


class ScraperMedicineTestCase(TestCase):
    @patch('api.scraper.scraper_medicine_post.LegalBasesSerializer', is_valid=True)
    @patch('api.scraper.scraper_medicine_post.EUOrphanConSerializer', is_valid=True)
    @patch('api.scraper.scraper_medicine_post.PrimeSerializer', is_valid=True)
    @patch('api.scraper.scraper_medicine_post.OrphanDesignationSerializer', is_valid=True)
    @patch('api.scraper.scraper_medicine_post.MAHSerializer', is_valid=True)
    @patch('api.scraper.scraper_medicine_post.BrandNameSerializer', is_valid=True)
    @patch('api.scraper.scraper_medicine_post.AuthorisationTypeSerializer', is_valid=True)
    @patch('api.scraper.scraper_medicine_post.AuthorisationStatusSerializer', is_valid=True)
    @patch('api.scraper.scraper_medicine_post.MedicineSerializer', is_valid=True)
    def test_scraper_post_new(self, medicine_serializer, aut_status_serializer, aut_type_serializer,
                              brand_name_serializer, mah_serializer, od_serializer,
                              prime_serializer, eu_oc_serializer, legal_base_serializer):
        """
        Test posting a new medicine to the scraper post function

        Args:
            medicine_serializer (MagicMock): The mock object for the MedicineSerializer
            aut_status_serializer (MagicMock): The mock object for the AuthorisationStatusSerializer
            aut_type_serializer (MagicMock): The mock object for the AuthorisationTypeSerializer
            brand_name_serializer (MagicMock): The mock object for the BrandNameSerializer
            mah_serializer (MagicMock): The mock object for the MAHSerializer
            od_serializer (MagicMock): The mock object for the OrphanDesignationSerializer
            prime_serializer (MagicMock): The mock object for the PrimeSerializer
            eu_oc_serializer (MagicMock): The mock object for the EUOrphanConSerializer
            legal_base_serializer (MagicMock): The mock object for the LegalBasesSerializer
        """
        self.data = {
            "data": [
                {
                    "eu_pnumber": "13",
                    "active_substance": "testsubstance",
                    "eu_nas": True,
                    "ema_procedure_start_initial": "2019-01-28",
                    "chmp_opinion_date": "2019-02-28",
                    "eu_aut_date": "2019-03-28",
                    "eu_legal_basis": ["article 4.8"],
                    "ema_url": "https://ema.com",
                    "ec_url": "https://ec.com",
                    "ema_number": "23",
                    "eu_med_type": "test_type",
                    "eu_atmp": False,
                    "aut_url": "https://aut.com",
                    "smpc_url": "https://smpc.com",
                    "epar_url": "https://epar.com",
                    "atc_code": "atccode",
                    "ema_number_check": True,
                    "ema_rapp": "Germany",
                    "ema_corapp": "France",
                    "eu_accel_assess_g": False,
                    "eu_accel_assess_m": True,
                    "assess_time_days_total": 100,
                    "assess_time_days_active": 80,
                    "assess_time_days_cstop": 20,
                    "ec_decision_time_days": 10,
                    "ema_reexamination": True,
                    "eu_referral": False,
                    "eu_suspension": False,
                    "omar_url": "https://omar.com",
                    "odwar_url": "https://odwar.com",
                    "eu_od_number": "EU/od_number",
                    "ema_od_number": "EMA/od_number",
                    "eu_od_con": "test eu od con",
                    "eu_od_date": "2018-09-01",
                    "eu_od_pnumber": "1 million",
                    "eu_od_sponsor": "test eu od sponsor",
                    "eu_od_comp_date": "2018-09-02",
                    "eu_aut_type": [
                        {
                            "eu_aut_type": "CONDITIONAL",
                            "change_date": "2019-05-28",
                        }
                    ],
                    "eu_aut_status": [
                        {
                            "eu_aut_status": "ACTIVE",
                            "change_date": "2019-06-28",
                        }
                    ],
                    "eu_brand_name": [
                        {
                            "eu_brand_name": "brandname",
                            "change_date": "2019-07-28",
                        }
                    ],
                    "eu_od": [
                        {
                            "eu_od": True,
                            "change_date": "2019-08-28",
                        }
                    ],
                    "eu_prime": [
                        {
                            "eu_prime": False,
                            "change_date": "2019-09-28",
                        }
                    ],
                    "eu_mah": [
                        {
                            "eu_mah": "eu_mahtest",
                            "change_date": "2019-10-28",
                        }
                    ],
                    "eu_orphan_con": [
                        {
                            "eu_orphan_con": "Zynteglo",
                            "change_date": "2019-12-28",
                        }
                    ],
                }
            ]
        }

        scraper = ScraperMedicine()
        scraper.post(self)

        # Test if data gets passed correctly to MedicineSerializer
        medicine_data = medicine_serializer.call_args.kwargs["data"]
        medicine_expected = self.data["data"][0]
        self.assertEqual(sorted(dict(medicine_data).items()), sorted(medicine_expected.items()))

        # Test if data gets passed correctly to history serializers
        aut_type_data = aut_type_serializer.call_args.args[1]
        aut_type_expected = {
            "eu_pnumber": "13",
            "eu_aut_type": "CONDITIONAL",
            "change_date": "2019-05-28",
        }
        self.assertEqual(sorted(dict(aut_type_data).items()), sorted(aut_type_expected.items()))

        aut_status_data = aut_status_serializer.call_args.args[1]
        aut_status_expected = {
            "eu_pnumber": "13",
            "eu_aut_status": "ACTIVE",
            "change_date": "2019-06-28",
        }
        self.assertEqual(sorted(dict(aut_status_data).items()), sorted(aut_status_expected.items()))

        eu_brand_name_data = brand_name_serializer.call_args.args[1]
        eu_brand_name_expected = {
            "eu_pnumber": "13",
            "eu_brand_name": "brandname",
            "change_date": "2019-07-28",
        }
        self.assertEqual(sorted(dict(eu_brand_name_data).items()), sorted(eu_brand_name_expected.items()))

        eu_od_data = od_serializer.call_args.args[1]
        eu_od_expected = {
            "eu_pnumber": "13",
            "eu_od": True,
            "change_date": "2019-08-28",
        }
        self.assertEqual(sorted(dict(eu_od_data).items()), sorted(eu_od_expected.items()))

        eu_prime_data = prime_serializer.call_args.args[1]
        eu_prime_expected = {
            "eu_pnumber": "13",
            "eu_prime": False,
            "change_date": "2019-09-28",
        }
        self.assertEqual(sorted(dict(eu_prime_data).items()), sorted(eu_prime_expected.items()))

        eu_mah_data = mah_serializer.call_args.args[1]
        eu_mah_expected = {
            "eu_pnumber": "13",
            "eu_mah": "eu_mahtest",
            "change_date": "2019-10-28",
        }
        self.assertEqual(sorted(dict(eu_mah_data).items()), sorted(eu_mah_expected.items()))

        eu_orphan_con_data = eu_oc_serializer.call_args.args[1]
        eu_orphan_con_expected = {
            "eu_pnumber": "13",
            "eu_orphan_con": "Zynteglo",
            "change_date": "2019-12-28",
        }
        self.assertEqual(sorted(dict(eu_orphan_con_data).items()), sorted(eu_orphan_con_expected.items()))

        eu_legal_basis_data = legal_base_serializer.call_args.args[1]
        eu_legal_basis_expected = {
            "eu_pnumber": "13",
            "eu_legal_basis": "article 4.8",
        }
        self.assertEqual(sorted(dict(eu_legal_basis_data).items()), sorted(eu_legal_basis_expected.items()))

    @patch('api.scraper.scraper_medicine_post.PrimeSerializer', is_valid=True)
    @patch('api.scraper.scraper_medicine_post.AuthorisationStatusSerializer', is_valid=True)
    @patch('api.scraper.scraper_medicine_post.MedicineFlexVarUpdateSerializer', is_valid=True)
    def test_scraper_post_update(self, update_serializer, aut_status_serializer, prime_serializer):
        """
        Test posting an update to an existing medicine to the scraper post function

        Args:
            update_serializer (MagicMock): The mock object for the MedicineFlexVarUpdateSerializer
            aut_status_serializer (MagicMock): The mock object for the AuthorisationStatusSerializer
            prime_serializer (MagicMock): The mock object for the PrimeSerializer
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

        # data to be updated by the scraper post endpoint
        self.data = {
            "data": [
                {
                    "eu_pnumber": "15",
                    "active_substance": "new substance",
                    "ema_url": "https://newemaurl.com",
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

        medicine_data = update_serializer.call_args.kwargs["data"]

        # test if MedicineFlexVarUpdateSerializer has been called correctly
        self.assertEqual(self.data["data"][0], medicine_data)

        # test if AuthorisationStatusSerializer has been called correctly
        eu_aut_status_data = aut_status_serializer.call_args.args[1]
        eu_aut_status_expected = {
            "eu_pnumber": "15",
            "eu_aut_status": "WITHDRAWN",
            "change_date": "2023-01-01",
        }
        self.assertEqual(sorted(dict(eu_aut_status_data).items()), sorted(eu_aut_status_expected.items()))

        # test if PrimeSerializer has been called correctly
        eu_prime_data = prime_serializer.call_args.args[1]
        eu_prime_expected = {
            "eu_pnumber": "15",
            "eu_prime": False,
            "change_date": "2023-01-02",
        }
        self.assertEqual(sorted(dict(eu_prime_data).items()), sorted(eu_prime_expected.items()))

    def test_scraper_post_new_missing_history(self):
        """
        Test if the scraper post endpoint correctly refuses new medicine with missing history attribute
        """
        # This data has the eu_orphan_con history attribute missing
        self.data = {
            "override": False,
            "data": [
                {
                    "eu_pnumber": "14",
                    "active_substance": "testsubstance",
                    "eu_nas": True,
                    "ema_procedure_start_initial": "2019-01-28",
                    "chmp_opinion_date": "2019-02-28",
                    "eu_aut_date": "2019-03-28",
                    "eu_legal_basis": ["article 4.8"],
                    "ema_url": "https://ema.com",
                    "ec_url": "https://ec.com",
                    "ema_number": "23",
                    "eu_med_type": "test_type",
                    "eu_atmp": False,
                    "aut_url": "https://aut.com",
                    "smpc_url": "https://smpc.com",
                    "epar_url": "https://epar.com",
                    "atc_code": "atccode",
                    "ema_number_check": True,
                    "ema_rapp": "Germany",
                    "ema_corapp": "France",
                    "eu_accel_assess_g": False,
                    "eu_accel_assess_m": True,
                    "assess_time_days_total": 100,
                    "assess_time_days_active": 80,
                    "assess_time_days_cstop": 20,
                    "ec_decision_time_days": 10,
                    "ema_reexamination": True,
                    "eu_referral": False,
                    "eu_suspension": False,
                    "omar_url": "https://omar.com",
                    "odwar_url": "https://odwar.com",
                    "eu_od_number": "EU/od_number",
                    "ema_od_number": "EMA/od_number",
                    "eu_od_con": "test eu od con",
                    "eu_od_date": "2018-09-01",
                    "eu_od_pnumber": "1 million",
                    "eu_od_sponsor": "test eu od sponsor",
                    "eu_od_comp_date": "2018-09-02",
                    "eu_aut_type": [
                        {
                            "eu_aut_type": "CONDITIONAL",
                            "change_date": "2019-05-28",
                        }
                    ],
                    "eu_aut_status": [
                        {
                            "eu_aut_status": "ACTIVE",
                            "change_date": "2019-06-28",
                        }
                    ],
                    "eu_brand_name": [
                        {
                            "eu_brand_name": "brandname",
                            "change_date": "2019-07-28",
                        }
                    ],
                    "eu_od": [
                        {
                            "eu_od": True,
                            "change_date": "2019-08-28",
                        }
                    ],
                    "eu_prime": [
                        {
                            "eu_prime": False,
                            "change_date": "2019-09-28",
                        }
                    ],
                    "eu_mah": [
                        {
                            "eu_mah": "eu_mahtest",
                            "change_date": "2019-10-28",
                        }
                    ],
                }
            ]
        }

        scraper = ScraperMedicine()
        response = scraper.post(self)

        # Assert response returns failed medicine
        self.data["data"][0]["errors"] = "eu_orphan_con must be part of the data posted!"
        self.assertEqual(self.data["data"], response.data)
