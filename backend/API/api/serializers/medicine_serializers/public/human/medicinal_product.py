# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

"""
This serializer is responsible for serializing all medicine data.
The medicine data is spread out over several tables in the database and therefore this serializer file
has to access all different tables and merge all this data in a one dimensional object.
"""

from rest_framework import serializers
from api.serializers.medicine_serializers.public.common import (
    RelatedMixin,
    ListMixin,
    HistoryMixin,
    AnyBoolsList,
)
from api.models.human_models import (
    MedicinalProduct,
    LegalBases,
    IngredientsAndSubstances,
)
from api.serializers.medicine_serializers.public.human import (
    MarketingAuthorisationSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
    ProceduresSerializer,
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
        exclude = ("id", )


class HistoryEUOrphanConSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryEUOrphanCon` model.
    """
    class Meta:
        """
        Meta information
        """
        model = MedicinalProduct
        exclude = ("id", )


class PublicMedicinalProductSerializer(RelatedMixin, ListMixin, HistoryMixin, AnyBoolsList, serializers.ModelSerializer):
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
        # serializers to be added as an initial history variable and flattened
        initial_history = [
            ("eu_brand_name_initial", BrandNameSerializer),
            ("eu_od_initial", OrphanDesignationSerializer),
            ("eu_prime_initial", PrimeSerializer),
        ]
        # serializers to be added as a current history variable and flattened
        current_history = [
            ("eu_aut_status", AuthorisationStatusSerializer),
            ("eu_aut_type", AuthorisationTypeSerializer),
            ("eu_brand_name", BrandNameSerializer),
            ("eu_mah", MAHSerializer),
            ("eu_od", OrphanDesignationSerializer),
            ("eu_prime", PrimeSerializer),
        ]
        any_bools_list = [
            ("procedures", ProceduresSerializer, ["eu_referral", "eu_suspension"]),
        ]
