from rest_framework import serializers
from api.models.orphan_models import (
    HistoryEUOrphanCon,
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
