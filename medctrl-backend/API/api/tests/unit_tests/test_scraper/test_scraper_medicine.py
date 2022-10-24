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
)
from api.serializers.medicine_serializers.scraper import (
    MedicineSerializer,
    MedicineFlexVarUpdateSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
    EUOrphanConSerializer,
)

class ScraperMedicineTestCase(TestCase):
    def setUp(self):
        self.data = {
            "override": False,
            "data": [
                {
                    "eu_pnumber": "13",
                    "active_substance": "testsubstance",
                    "eu_nas": True,
                    "ema_procedure_start_initial": "2019-01-28",
                    "chmp_opinion_date": "2019-02-28",
                    "eu_aut_date": "2019-03-28",
                    "eu_legal_basis": "article 4.8",
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
                    "eu_aut_type": {
                        "eu_aut_type": "CONDITIONAL",
                        "change_date": "2019-05-28",
                    },
                    "eu_aut_status": {
                        "eu_aut_status": "ACTIVE",
                        "change_date": "2019-06-28",
                    },
                    "eu_brand_name": {
                        "eu_brand_name": "brandname",
                        "change_date": "2019-07-28",
                    },
                    "eu_od": {
                        "eu_od": True,
                        "change_date": "2019-08-28",
                    },
                    "eu_prime": {
                        "eu_prime": False,
                        "change_date": "2019-09-28",
                    },
                    "eu_mah": {
                        "eu_mah": "eu_mahtest",
                        "change_date": "2019-10-28",
                    },
                    "eu_orphan_con": {
                        "eu_orphan_con": "Zynteglo",
                        "change_date": "2019-12-28",
                    },
                }
            ]
        }

    def test_scraper_post_new(self):
        scraper = ScraperMedicine()
        scraper.post(self)

        medicine_query = Medicine.objects.first()
        medicine_data = MedicineSerializer(medicine_query).data
        medicine_expected = {
            "eu_pnumber": "13",
            "active_substance": "testsubstance",
            "eu_nas": True,
            "ema_procedure_start_initial": "2019-01-28",
            "chmp_opinion_date": "2019-02-28",
            "eu_aut_date": "2019-03-28",
            "eu_legal_basis": "article 4.8",
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
        }
        self.assertEqual(sorted(dict(medicine_data).items()), sorted(medicine_expected.items()))

        aut_type_query = HistoryAuthorisationType.objects.first()
        aut_type_data = AuthorisationTypeSerializer(aut_type_query).data
        aut_type_expected = {
            "eu_pnumber": "13",
            "eu_aut_type": "CONDITIONAL",
            "change_date": "2019-05-28",
        }
        self.assertEqual(sorted(dict(aut_type_data).items()), sorted(aut_type_expected.items()))

        aut_status_query = HistoryAuthorisationStatus.objects.first()
        aut_status_data = AuthorisationStatusSerializer(aut_status_query).data
        aut_status_expected = {
            "eu_pnumber": "13",
            "eu_aut_status": "ACTIVE",
            "change_date": "2019-06-28",
        }
        self.assertEqual(sorted(dict(aut_status_data).items()), sorted(aut_status_expected.items()))

        eu_brand_name_query = HistoryBrandName.objects.first()
        eu_brand_name_data = BrandNameSerializer(eu_brand_name_query).data
        eu_brand_name_expected = {
            "eu_pnumber": "13",
            "eu_brand_name": "brandname",
            "change_date": "2019-07-28",
        }
        self.assertEqual(sorted(dict(eu_brand_name_data).items()), sorted(eu_brand_name_expected.items()))

        eu_od_query = HistoryOD.objects.first()
        eu_od_data = OrphanDesignationSerializer(eu_od_query).data
        eu_od_expected = {
            "eu_pnumber": "13",
            "eu_od": True,
            "change_date": "2019-08-28",
        }
        self.assertEqual(sorted(dict(eu_od_data).items()), sorted(eu_od_expected.items()))

        eu_prime_query = HistoryPrime.objects.first()
        eu_prime_data = PrimeSerializer(eu_prime_query).data
        eu_prime_expected = {
            "eu_pnumber": "13",
            "eu_prime": False,
            "change_date": "2019-09-28",
        }
        self.assertEqual(sorted(dict(eu_prime_data).items()), sorted(eu_prime_expected.items()))

        eu_mah_query = HistoryMAH.objects.first()
        eu_mah_data = MAHSerializer(eu_mah_query).data
        eu_mah_expected = {
            "eu_pnumber": "13",
            "eu_mah": "eu_mahtest",
            "change_date": "2019-10-28",
        }
        self.assertEqual(sorted(dict(eu_mah_data).items()), sorted(eu_mah_expected.items()))

        eu_orphan_con_query = HistoryEUOrphanCon.objects.first()
        eu_orphan_con_data = EUOrphanConSerializer(eu_orphan_con_query).data
        eu_orphan_con_expected = {
            "eu_pnumber": "13",
            "eu_orphan_con": "Zynteglo",
            "change_date": "2019-12-28",
        }
        self.assertEqual(sorted(dict(eu_orphan_con_data).items()), sorted(eu_orphan_con_expected.items()))
