from django.test import TestCase
from api.models.medicine_models import (
    Medicine,
    HistoryATCCode,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryEMANumberCheck,
    HistoryOD,
    HistoryPrime,
)
from api.models.medicine_models.common import (
    AutStatus,
    AutTypes,
    LegalBases
)

from api.serializers.medicine_serializers.public import PublicMedicineSerializer


class PublicMedicineSerializerTestCase(TestCase):
    def setUp(self):
        medicine = Medicine(
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
            epar_url="eparurl.com"
        )
        medicine.save()
        self.medicine = medicine
        HistoryATCCode.objects.create(
            atc_code_id=1,
            eu_pnumber=medicine,
            change_date="2022-01-01",
            atc_code="C03CA01",
        )
        HistoryAuthorisationType.objects.create(
            eu_aut_type_id=1,
            eu_pnumber=medicine,
            change_date="2022-01-02",
            eu_aut_type="12345678910",
        )
        HistoryAuthorisationStatus.objects.create(
            eu_aut_status_id=1,
            eu_pnumber=medicine,
            change_date="2022-01-03",
            eu_aut_status=AutStatus.ACTIVE,
        )
        HistoryBrandName.objects.create(
            eu_brand_name_id=1,
            eu_pnumber=medicine,
            change_date="2022-01-04",
            eu_brand_name="Brand Name",
        )
        HistoryOD.objects.create(
            eu_od_id=1,
            eu_pnumber=medicine,
            change_date="2022-01-05",
            eu_od=True,
        )
        HistoryPrime.objects.create(
            eu_prime_id=1,
            eu_pnumber=medicine,
            change_date="2022-01-06",
            eu_prime=False,
        )
        HistoryMAH.objects.create(
            eu_mah_id=1,
            eu_pnumber=medicine,
            change_date="2022-01-07",
            eu_mah="MAH",
        )
        HistoryEMANumberCheck.objects.create(
            ema_number_check_id=1,
            eu_pnumber=medicine,
            change_date="2022-01-08",
            ema_number_check=True,
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
            "atc_code": "C03CA01",
            "eu_aut_status": "ACTIVE",
            "eu_aut_type": "12345678910",
            "eu_brand_name": "Brand Name",
            "eu_mah": "MAH",
            "ema_number_check": True,
            "eu_od": True,
            "eu_prime": False,
        }
        self.assertEqual(data, expected)
