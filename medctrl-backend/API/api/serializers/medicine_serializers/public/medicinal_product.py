# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

"""
This serializer is responsible for serializing all medicine data.
The medicine data is spread out over several tables in the database and therefore this serializer file
has to access all different tables and merge all this data in a one dimensional object.
"""

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
    This serializer serializes the :py:class:`.LegalBases` model.
    """

    class Meta:
        """
        Meta information
        """
        model = LegalBases
        fields = ("eu_legal_basis",)


class IngredientsAndSubstancesSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.IngredientsAndSubstances` model.
    """
    class Meta:
        """
        Meta information
        """
        model = IngredientsAndSubstances
        exclude = ["active_substance_hash", ]


class PublicMedicinalProductSerializer(RelatedMixin, ListMixin, HistoryMixin, serializers.ModelSerializer):
    """
    This serializer serializers all the needed data for the medicine view from the :py:class:`.MedicinalProduct` model.
    """
    class Meta:
        """
        Meta information
        """
        model = MedicinalProduct
        exclude = ("ema_number_check",)
        # Serializers to be added and flattened
        related = [
            ("ingredients_and_substances", IngredientsAndSubstancesSerializer),
            ("marketing_authorisation", MarketingAuthorisationSerializer),
        ]
        # serializers to be added as a list and flattened
        list = [
            ("eu_legal_basis", LegalBasesSerializer),
        ]
        # serializer to be added as a history variable and flattened
        history = [
            ("eu_aut_status", AuthorisationStatusSerializer, False, True),
            ("eu_aut_type", AuthorisationTypeSerializer, True, True),
            ("eu_brand_name", BrandNameSerializer, True, True),
            ("eu_mah", MAHSerializer, True, True),
            ("eu_od", OrphanDesignationSerializer, True, False),
            ("eu_prime", PrimeSerializer, True, False),
        ]
