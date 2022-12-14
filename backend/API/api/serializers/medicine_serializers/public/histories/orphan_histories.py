# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from collections import OrderedDict
from django.db.models import Model
from typing import Any
from rest_framework import serializers
from api.models.orphan_models import (
    HistoryEUOrphanCon,
    HistoryEUODSponsor,
)


class EUOrphanConSerializer (serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryEUOrphanCon` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryEUOrphanCon
        fields = ("indication", "link_date", "end_date", "change_date", )

    def to_representation(self, obj: Model) -> OrderedDict[str, Any]:
        representation = super().to_representation(obj)
        change_date = representation.pop("change_date")
        return OrderedDict([("eu_orphan_con", representation), ("change_date", change_date)])


class EUODSponsorSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryEUODSponsor` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryEUODSponsor
        fields = ("eu_od_sponsor", "change_date", )
