# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all serializers concerning
# the history of the medicine data of the database.
#---------------------------------------------

from rest_framework import serializers
from api.models.medicine_models import (
    Historybrandname,
    Historymah,
    Historyorphan,
    Historyprime,
)


class BrandnameSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = Historybrandname
        fields = "__all__"


class MAHSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = Historymah
        fields = "__all__"


class OrphanSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = Historyorphan
        fields = "__all__"


class PRIMESerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = Historyprime
        fields = "__all__"
