from rest_framework import serializers
from api.models import Medicine, Substance, LegalBasis, LegalScope, AtcCode


class LegalBasisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalBasis
        fields = ["description"]


class LegalScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalScope
        fields = ["description"]


class AtcCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtcCode
        fields = ["atc_code", "description"]


class MedicineSerializer(serializers.ModelSerializer):
    legal_basis = (
        LegalBasisSerializer()
    )  # needs to be directly in legal_basis not legalbasis -> description
    legal_scope = (
        LegalScopeSerializer()
    )  # needs to be directly in legal_scope not legalscope -> description
    atc_code = AtcCodeSerializer()

    class Meta:
        model = Medicine
        fields = "__all__"
