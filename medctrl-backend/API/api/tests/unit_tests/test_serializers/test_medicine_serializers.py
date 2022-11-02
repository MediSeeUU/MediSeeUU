from django.test import TestCase
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

from api.serializers.medicine_serializers.public import PublicMedicineSerializer


class PublicMedicineSerializerTestCase(TestCase):
    def setUp(self):
        self.medicine = Medicine(
            eu_pnumber=1,
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
        HistoryAuthorisationType.objects.create(
            eu_pnumber=self.medicine,
            change_date="2021-01-02",
            eu_aut_type=AutTypes.EXCEPTIONAL,
        )

        HistoryAuthorisationStatus.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-03",
            eu_aut_status=AutStatus.ACTIVE,
        )
        HistoryAuthorisationStatus.objects.create(
            eu_pnumber=self.medicine,
            change_date="2021-01-03",
            eu_aut_status=AutStatus.WITHDRAWAL,
        )

        HistoryBrandName.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-04",
            eu_brand_name="Brand Name 1",
        )
        HistoryBrandName.objects.create(
            eu_pnumber=self.medicine,
            change_date="2021-01-04",
            eu_brand_name="Brand Name 2",
        )

        HistoryOD.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-05",
            eu_od=True,
        )
        HistoryOD.objects.create(
            eu_pnumber=self.medicine,
            change_date="2021-01-05",
            eu_od=False,
        )

        HistoryPrime.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-06",
            eu_prime=False,
        )
        HistoryPrime.objects.create(
            eu_pnumber=self.medicine,
            change_date="2021-01-06",
            eu_prime=True,
        )

        HistoryMAH.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-07",
            eu_mah="MAH 1",
        )
        HistoryMAH.objects.create(
            eu_pnumber=self.medicine,
            change_date="2021-01-07",
            eu_mah="MAH 2",
        )

        HistoryEUOrphanCon.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-08",
            eu_orphan_con="eu orphan con 1",
        )
        HistoryEUOrphanCon.objects.create(
            eu_pnumber=self.medicine,
            change_date="2021-01-08",
            eu_orphan_con="eu orphan con 2",
        )
        LegalBases.objects.create(
            eu_pnumber=self.medicine,
            eu_legal_basis=LegalBasesTypes.article10_a,
        )

    def test_public_medicine_serializer(self):
        data = PublicMedicineSerializer(self.medicine).data
        expected = {
            "eu_pnumber": "1",
            "active_substance": "ACTIVE SUBSTANCE",
            "eu_nas": True,
            "ema_procedure_start_initial": "2000-01-01",
            "chmp_opinion_date": "2000-01-02",
            "eu_aut_date": "2000-01-03",
            "eu_legal_basis": ["article 10(a)"],
            "ema_url": "emaurl.com",
            "ec_url": "ecurl.com",
            "ema_number": "1",
            "eu_med_type": "med",
            "eu_atmp": False,
            "aut_url": "auturl.com",
            "smpc_url": "smpcurl.com",
            "epar_url": "eparurl.com",
            "ema_number_check": True,
            "eu_od_initial": False,
            "eu_prime_initial": True,
            "ema_rapp": "ema rapp",
            "ema_corapp": "ema corapp",
            "eu_accel_assess_g": True,
            "eu_accel_assess_m": False,
            "assess_time_days_total": 10,
            "assess_time_days_active": 5,
            "assess_time_days_cstop": 2,
            "ec_decision_time_days": 1000,
            "ema_reexamination": False,
            "eu_referral": True,
            "eu_suspension": True,
            "omar_url": "omarurl.com",
            "odwar_url": "odwarurl.com",
            "eu_od_number": "8",
            "ema_od_number": "500",
            "eu_od_con": "eu od con",
            "eu_od_date": "2000-01-04",
            "eu_od_pnumber": "80",
            "eu_od_sponsor": "eu od sponsor",
            "eu_od_comp_date": "2000-01-05",
            "atc_code": "C03CA01",
            "eu_aut_status": "ACTIVE",
            "eu_aut_type_initial": "EXCEPTIONAL",
            "eu_aut_type_current": "STANDARD",
            "eu_brand_name_initial": "Brand Name 2",
            "eu_brand_name_current": "Brand Name 1",
            "eu_mah_initial": "MAH 2",
            "eu_mah_current": "MAH 1",
            "eu_orphan_con_initial": "eu orphan con 2",
            "eu_orphan_con_current": "eu orphan con 1",
        }
        self.assertDictEqual(data, expected)
