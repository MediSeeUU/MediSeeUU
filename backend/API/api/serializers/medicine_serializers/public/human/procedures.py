# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

"""
This serializer is responsible for serializing all procedure data.
The procedure data is spread out over several tables in the database and therefore this serializer file
has to access all different tables and merge all this data in a one dimensional object.
"""

from rest_framework import serializers
from api.models.human_models import (
    Procedures,
)


class ProceduresSerializer(serializers.ModelSerializer):
    """
    This serializer serializers all the needed data for the medicine view from the :py:class:`.Procedures` model.
    """

    class Meta:
        """
        Meta information
        """
        model = Procedures
        exclude = ("id", "eu_pnumber", )
