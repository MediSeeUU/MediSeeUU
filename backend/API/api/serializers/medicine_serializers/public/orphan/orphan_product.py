# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

"""
This serializer is responsible for serializing all orphan product data.
The orphan product data is spread out over several tables in the database and therefore this serializer file
has to access all different tables and merge all this data in a one dimensional object.
"""

from rest_framework import serializers
from api.serializers.medicine_serializers.public.common import (
    HistoryMixin,
)
from api.models.orphan_models import (
    OrphanProduct,
)
from api.serializers.medicine_serializers.public.orphan import (
    EUODSponsorSerializer,
)


class OrphanProductSerializer(HistoryMixin, serializers.ModelSerializer):
    """
    This serializer serializers all the needed data for the medicine view from the :py:class:`.OrphanProduct` model.
    """

    class Meta:
        """
        Meta information
        """
        model = OrphanProduct
        exclude = ("eu_orphan_con_initial",)
        current_history = [
            ("eu_od_sponsor", EUODSponsorSerializer),
        ]
