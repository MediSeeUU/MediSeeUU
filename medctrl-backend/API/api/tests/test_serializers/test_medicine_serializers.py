from django.test import TestCase
from api.models.medicine_models import (
    Medicine,
    HistoryATCCode,
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

from api.serializers.medicine_serializers.public import PublicMedicineSerializer


class PublicMedicineSerializerTestCase(TestCase):
    def setUp(self):
        self.medicine = Medicine(
            eu_pnumber=1,
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
        HistoryATCCode.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-01",
            atc_code="C03CA01",
        )
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
            eu_brand_name="Brand Name",
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
            eu_mah="MAH",
        )
        HistoryEUOrphanCon.objects.create(
            eu_pnumber=self.medicine,
            change_date="2022-01-08",
            eu_orphan_con="eu orphan con",
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
            "eu_legal_basis": "article 10(a)",
            "ema_url": "emaurl.com",
            "ec_url": "ecurl.com",
            "ema_number": "1",
            "eu_med_type": "med",
            "eu_atmp": False,
            "aut_url": "auturl.com",
            "smpc_url": "smpcurl.com",
            "epar_url": "eparurl.com",
            "ema_number_check": True,
            "eu_od": True,
            "eu_prime": False,
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
            "eu_aut_type": "STANDARD",
            "eu_brand_name": "Brand Name",
            "eu_mah_initial": "MAH",
            "eu_mah_current": "MAH",
            "eu_orphan_con": "eu orphan con",
        }
        self.assertEqual(data, expected)
