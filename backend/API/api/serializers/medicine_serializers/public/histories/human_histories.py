# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from collections import OrderedDict
from typing import Any
from django.db.models import Model
from rest_framework import serializers
from api.serializers.medicine_serializers.public.common import (
    ManyRelatedMixin,
)
from api.models.human_models import (
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
)
from api.models.orphan_models import (
    OrphanProduct,
    HistoryEUOrphanCon,
)


class AuthorisationStatusSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryAuthorisationStatus` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryAuthorisationStatus
        fields = ("eu_aut_status", "change_date", )


class AuthorisationTypeSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryAuthorisationType` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryAuthorisationType
        fields = ("eu_aut_type", "change_date", )


class BrandNameSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryBrandName` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryBrandName
        fields = ("eu_brand_name", "change_date", )


class MAHSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryMAH` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryMAH
        fields = ("eu_mah", "change_date", )


class OrphanDesignationSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryOD` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryOD
        fields = ("eu_od", "change_date", )


class PrimeSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryPrime` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryPrime
        fields = ("eu_prime", "change_date", )


class HistoryEUOrphanConSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryEUOrphanCon` model.
    """

    class Meta:
        """
        Meta information
        """
        model = HistoryEUOrphanCon
        exclude = ("id",)


def transform_eu_orphan_con(data):
    transformed_data = []
    for item in data:
        change_date = item.pop("change_date")
        transformed_item = OrderedDict([("eu_orphan_con", item), ("change_date", change_date)])
        transformed_data.append(transformed_item)
    return transformed_data


class EUOrphanConSerializer(ManyRelatedMixin, serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryEUOrphanCon` model.
    """

    class Meta:
        """
        Meta information
        """
        model = OrphanProduct
        fields = ()
        many_related = [
            ("eu_orphan_con", HistoryEUOrphanConSerializer, transform_eu_orphan_con)
        ]

    def to_representation(self, obj: Model) -> OrderedDict[str, Any]:
        representation = super().to_representation(obj)
        return representation
