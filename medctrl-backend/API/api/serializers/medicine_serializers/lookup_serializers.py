# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file conatins all serializers concerning the lookup tables
# in the database.
# -------------------------------------------------------

from rest_framework import serializers
from api.models.medicine_models import (
    Lookupactivesubstance,
    Lookupatccode,
    Lookuplegalbasis,
    Lookuplegalscope,
    Lookupmedicinetype,
    Lookupstatus,
    Lookuprapporteur,
    Lookupproceduretype,
)


class LookupActiveSubstanceSerializer(serializers.ModelSerializer):
    """
    Lookup table active substance serializer for the scraper endpoints
    """

    class Meta:
        model = Lookupactivesubstance
        fields = "__all__"


class LookupAtccodeSerializer(serializers.ModelSerializer):
    """
    Lookup table atc code serializer for the scraper endpoints
    """

    class Meta:
        model = Lookupatccode
        fields = "__all__"


class LookupLegalbasisSerializer(serializers.ModelSerializer):
    """
    Lookup table legal basis serializer for the scraper endpoints
    """

    class Meta:
        model = Lookuplegalbasis
        fields = "__all__"


class LookupLegalscopeSerializer(serializers.ModelSerializer):
    """
    Lookup table legal scope serializer for the scraper endpoints
    """

    class Meta:
        model = Lookuplegalscope
        fields = "__all__"


class LookupMedicinetypeSerializer(serializers.ModelSerializer):
    """
    Lookup table medicinetype serializer for the scraper endpoints
    """

    class Meta:
        model = Lookupmedicinetype
        fields = "__all__"


class LookupStatusSerializer(serializers.ModelSerializer):
    """
    Lookup table status serializer for the scraper endpoints
    """

    class Meta:
        model = Lookupstatus
        fields = "__all__"


class LookupRapporteurSerializer(serializers.ModelSerializer):
    """
    Lookup table rapporteur serializer for the scraper endpoints
    """

    class Meta:
        model = Lookuprapporteur
        fields = "__all__"


class LookupProceduretypeSerializer(serializers.ModelSerializer):
    """
    Lookup table proceduretype serializer for the scraper endpoints
    """

    class Meta:
        model = Lookupproceduretype
        fields = "__all__"
