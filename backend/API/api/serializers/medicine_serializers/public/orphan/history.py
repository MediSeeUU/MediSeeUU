from rest_framework import serializers
from api.models.orphan_models import (
    HistoryEUOrphanCon,
    HistoryEUODSponsor,
)


class EUOrphanConSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryEUOrphanCon` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryEUOrphanCon
        fields = ("eu_orphan_con",)


class EUODSponsorSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the :py:class:`.HistoryEUODSponsor` model.
    """
    class Meta:
        """
        Meta information
        """
        model = HistoryEUODSponsor
        fields = ("eu_od_sponsor",)
