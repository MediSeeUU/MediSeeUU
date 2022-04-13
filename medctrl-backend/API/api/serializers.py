# from rest_framework import serializers
# from api.models import Medicine, LegalBasis, LegalScope, AtcCode, Procedure

# class LegalBasisSerializer(serializers.ModelSerializer):
#     """Legal basis serializer"""

#     class Meta:
#         """Metadata"""

#         model = LegalBasis
#         fields = ["description"]


# class LegalScopeSerializer(serializers.ModelSerializer):
#     """Legal scope serializer"""

#     class Meta:
#         """Metadata"""

#         model = LegalScope
#         fields = ["description"]


# class AtcCodeSerializer(serializers.ModelSerializer):
#     """Atc code serializer"""

#     class Meta:
#         """Metadata"""

#         model = AtcCode
#         fields = ["atc_code", "description"]


# class MedicineSerializer(serializers.ModelSerializer):
#     """Medicine serializer"""

#     legal_basis = (
#         LegalBasisSerializer()
#     )  # needs to be directly in legal_basis not legalbasis -> description
#     legal_scope = (
#         LegalScopeSerializer()
#     )  # needs to be directly in legal_scope not legalscope -> description
#     atc_code = AtcCodeSerializer()

#     class Meta:
#         """Metadata"""

#         model = Medicine
#         fields = "__all__"


# class ProcedureSerializer(serializers.ModelSerializer):
#     """Endpoint procedure serializer"""

#     class Meta:
#         """Metadata"""

#         model = Procedure
#         fields = "__all__"
#