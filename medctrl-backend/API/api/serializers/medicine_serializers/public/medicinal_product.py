# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This serializer is responsible for serializing all
# medicine data. The medicine data is spread out over
# several tables in the database and therefore this
# serializer file has to access all different tables
# and merge all this data in an onedimensional object.
# ---------------------------------------------------

from rest_framework import serializers
from api.serializers.medicine_serializers.common import (
    RelatedMixin,
    ListMixin,
    HistoryMixin,
)
from api.models.medicine_models import (
    MedicinalProduct,
    LegalBases,
    IngredientsAndSubstances,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
)
from api.serializers.medicine_serializers.public import (
    MarketingAuthorisationSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
)


class LegalBasesSerializer(serializers.ModelSerializer):
    """
    Legal bases table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """
        model = LegalBases
        fields = ("eu_legal_basis",)


class IngredientsAndSubstancesSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Meta information
        """
        model = IngredientsAndSubstances
        exclude = ["active_substance_hash", ]


class PublicMedicinalProductSerializer(RelatedMixin, ListMixin, HistoryMixin, serializers.ModelSerializer):
    """
    This is the view endpoint for a medicine.
    """
    class Meta:
        """
        Meta information
        """
        model = MedicinalProduct
        fields = "__all__"
        # Serializers to be added and flattened
        related = [
            ("ingredients_and_substances", IngredientsAndSubstancesSerializer),
            ("marketing_authorisation", MarketingAuthorisationSerializer),
        ]
        list = [
            ("eu_legal_basis", LegalBasesSerializer),
        ]
        history = [
            ("eu_aut_status", AuthorisationStatusSerializer, HistoryAuthorisationStatus),
            ("eu_aut_type_initial", AuthorisationTypeSerializer, HistoryAuthorisationType),
            ("eu_aut_type_current", AuthorisationTypeSerializer, HistoryAuthorisationType),
            ("eu_brand_name_initial", BrandNameSerializer, HistoryBrandName),
            ("eu_brand_name_current", BrandNameSerializer, HistoryBrandName),
            ("eu_mah_initial", MAHSerializer, HistoryMAH),
            ("eu_mah_current", MAHSerializer, HistoryMAH),
            ("eu_od_initial", OrphanDesignationSerializer, HistoryOD),
            ("eu_prime_initial", PrimeSerializer, HistoryPrime),
        ]
