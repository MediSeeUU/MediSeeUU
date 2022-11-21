from django.test import TestCase
from api.models.medicine_models import (
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
from api.models.medicine_models.common import (
    AutStatus,
    AutTypes,
    LegalBasesTypes,
)

from api.serializers.medicine_serializers.public import PublicMedicinalProductSerializer


class PublicMedicineSerializerTestCase(TestCase):
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

        HistoryAuthorisationType.objects.create(
            eu_pnumber_id="15",
            change_date="2022-01-02",
            eu_aut_type=AutTypes.STANDARD,
        )
        HistoryAuthorisationType.objects.create(
            eu_pnumber_id="15",
            change_date="2021-01-02",
            eu_aut_type=AutTypes.EXCEPTIONAL,
        )

        HistoryAuthorisationStatus.objects.create(
            eu_pnumber_id="15",
            change_date="2022-01-03",
            eu_aut_status=AutStatus.ACTIVE,
        )
        HistoryAuthorisationStatus.objects.create(
            eu_pnumber_id="15",
            change_date="2021-01-03",
            eu_aut_status=AutStatus.WITHDRAWAL,
        )

        HistoryBrandName.objects.create(
            eu_pnumber_id="15",
            change_date="2022-01-04",
            eu_brand_name="Brand Name 1",
        )
        HistoryBrandName.objects.create(
            eu_pnumber_id="15",
            change_date="2021-01-04",
            eu_brand_name="Brand Name 2",
        )

        HistoryOD.objects.create(
            eu_pnumber_id="15",
            change_date="2022-01-05",
            eu_od=True,
        )
        HistoryOD.objects.create(
            eu_pnumber_id="15",
            change_date="2021-01-05",
            eu_od=False,
        )

        HistoryPrime.objects.create(
            eu_pnumber_id="15",
            change_date="2022-01-06",
            eu_prime=False,
        )
        HistoryPrime.objects.create(
            eu_pnumber_id="15",
            change_date="2021-01-06",
            eu_prime=True,
        )

        HistoryMAH.objects.create(
            eu_pnumber_id="15",
            change_date="2022-01-07",
            eu_mah="MAH 1",
        )
        HistoryMAH.objects.create(
            eu_pnumber_id="15",
            change_date="2021-01-07",
            eu_mah="MAH 2",
        )

        LegalBases.objects.create(
            eu_pnumber_id="15",
            eu_legal_basis=LegalBasesTypes.article10_a,
        )

    def test_public_medicine_serializer(self):
        data = PublicMedicinalProductSerializer(self.medicine).data
        expected = {
            "eu_pnumber": "15",
            "active_substance": "ACTIVE SUBSTANCE",
            "atc_code": "C03CA01",
            "eu_nas": True,
            "ema_url": "emaurl.com",
            "ec_url": "ecurl.com",
            "ema_number": "1",
            "eu_med_type": "med",
            "eu_atmp": False,
            "eu_accel_assess_g": True,
            "eu_accel_assess_m": False,
            "assess_time_days_total": 10,
            "assess_time_days_active": 5,
            "assess_time_days_cstop": 2,
            "ec_decision_time_days": 1000,
            "ema_procedure_start_initial": "2000-01-01",
            "chmp_opinion_date": "2000-01-02",
            "eu_aut_date": "2000-01-03",
            "aut_url": "auturl.com",
            "smpc_url": "smpcurl.com",
            "epar_url": "eparurl.com",
            "ema_rapp": "ema rapp",
            "ema_corapp": "ema corapp",
            "ema_reexamination": False,
            "eu_legal_basis": ["article 10(a)"],
            "eu_od_initial": False,
            "eu_prime_initial": True,
            #"eu_referral": True,
            #"eu_suspension": True,
            "eu_aut_status": "ACTIVE",
            "eu_aut_type_initial": "EXCEPTIONAL",
            "eu_aut_type_current": "STANDARD",
            "eu_brand_name_initial": "Brand Name 2",
            "eu_brand_name_current": "Brand Name 1",
            "eu_mah_initial": "MAH 2",
            "eu_mah_current": "MAH 1",
        }
        self.assertDictEqual(data, expected)
