# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all serializers concerning
# the history of the medicine data of the database.
# ---------------------------------------------

from rest_framework import serializers
from api.models.orphan_models import (
    HistoryEUOrphanCon,
    HistoryEUODSponsor,
)


class EUOrphanConSerializer(serializers.ModelSerializer):
    """
    Orphan Condition table serializer for the post endpoint
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryEUOrphanCon
        exclude = ("id", )


class EUODSponsorSerializer(serializers.ModelSerializer):
    """
    Orphan sponsor table serializer for the post endpoint
    """

    class Meta:
        """
        Meta information
        """

        model = HistoryEUODSponsor
        exclude = ("id", )
