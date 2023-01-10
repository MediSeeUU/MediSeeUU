# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

"""
This serializer is responsible for serializing all medicine data.
The medicine data is spread out over several tables in the database and therefore this serializer file
has to access all different tables and merge all this data in a one dimensional object.
"""

from datetime import date, datetime
from rest_framework import serializers
from api.serializers.medicine_serializers.public.common import (
    RelatedMixin,
    ManyRelatedMixin,
    ListMixin,
    HistoryMixin,
    AnyBoolsList,
)
from api.models.human_models import (
    MedicinalProduct,
    LegalBases,
    IngredientsAndSubstances,
)
from api.models.orphan_models import (
    OrphanProduct,
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
    EUOrphanConSerializer,
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


class HistoryEUOrphanConSerializer(HistoryMixin, serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryEUOrphanCon` model.
    """
    class Meta:
        """
        Meta information
        """
        model = OrphanProduct
        fields = ("eu_orphan_con_initial", )
        initial_history = [
            ("eu_orphan_con_initial", EUOrphanConSerializer),
        ]
        current_history = [
            ("eu_orphan_con", EUOrphanConSerializer, "eu_orphan_con_current"),
        ]


def transform_eu_orphan_con(data):
    eu_orphan_con_initial = []
    eu_orphan_con_current = []

    most_current_change_date = date.min
    for orphan in data:
        if current_data := orphan.get("eu_orphan_con_current"):
            change_date = datetime.strptime(current_data.get("change_date"), "%Y-%m-%d").date()
            most_current_change_date = max(most_current_change_date, change_date)

    most_current_change_date = most_current_change_date.strftime("%Y-%m-%d")

    for orphan in data:
        if initial_data := orphan.get("eu_orphan_con_initial"):
            initial_data.pop("change_date", None)
            eu_orphan_con_initial.append(initial_data)
        if current_data := orphan.get("eu_orphan_con_current"):
            if current_data.get("change_date") == most_current_change_date:
                current_data.pop("change_date")
                eu_orphan_con_current.append(current_data)
    return {"eu_orphan_con_initial": eu_orphan_con_initial, "eu_orphan_con_current": eu_orphan_con_current}


class PublicMedicinalProductSerializer(RelatedMixin, ManyRelatedMixin,
                                       ListMixin, HistoryMixin, AnyBoolsList,
                                       serializers.ModelSerializer):
    """
    This serializer serializers all the needed data for the medicine view from the :py:class:`.MedicinalProduct` model.
    """
    class Meta:
        """
        Meta information
        """
        model = MedicinalProduct
        exclude = ()
        # Serializers to be added and flattened
        related = [
            ("ingredients_and_substances", IngredientsAndSubstancesSerializer),
            ("marketing_authorisation", MarketingAuthorisationSerializer),
        ]
        many_related = [
            ("eu_od_pnumber", HistoryEUOrphanConSerializer, transform_eu_orphan_con)
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
            ("eu_aut_status", AuthorisationStatusSerializer, "eu_aut_status"),
            ("eu_aut_type", AuthorisationTypeSerializer, "eu_aut_type_current"),
            ("eu_brand_name", BrandNameSerializer, "eu_brand_name_current"),
            ("eu_mah", MAHSerializer, "eu_mah_current"),
            ("eu_od", OrphanDesignationSerializer, "eu_od_current"),
            ("eu_prime", PrimeSerializer, "eu_prime_current"),
        ]
        any_bools_list = [
            ("procedures", ProceduresSerializer, ["eu_referral", "eu_suspension"]),
        ]
