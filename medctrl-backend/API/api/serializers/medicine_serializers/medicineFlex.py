from rest_framework import serializers

from api.models.medicine_models import Medicine
from api.serializers.medicine_serializers import (
    LegalBasisSerializer,
    AtcCodeSerializer,
    LegalScopeSerializer,
)


class MedicineFlexSerializer(serializers.ModelSerializer):
    """Medicine serializer"""

    """outdated serializer, to be replaced with what Lars is working on
    legal_basis = (
        LegalBasisSerializer()
    )  # needs to be directly in legal_basis not legalbasis -> description
    legal_scope = (
        LegalScopeSerializer()
    )  # needs to be directly in legal_scope not legalscope -> description
    atc_code = AtcCodeSerializer()
    """

    class Meta:
        """Metadata"""

        model = Medicine
        fields = ["atccode", "status", "referral", "suspension", "emaurl", "ecurl"]
