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

# serializer for active substance lookup table
class LookupActiveSubstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookupactivesubstance
        fields = "__all__"


# serializer for atc code lookup table
class LookupAtccodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookupatccode
        fields = "__all__"


# serializer for legal basis lookup table
class LookupLegalbasisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookuplegalbasis
        fields = "__all__"


# serializer for legal scope lookup table
class LookupLegalscopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookuplegalscope
        fields = "__all__"


# serializer for medicinetype lookup table
class LookupMedicinetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookupmedicinetype
        fields = "__all__"


# serializer for status lookup table
class LookupStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookupstatus
        fields = "__all__"


# serializer for rapporteur lookup table
class LookupRapporteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookuprapporteur
        fields = "__all__"


# serializer for proceduretype lookup table
class LookupProceduretypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookupproceduretype
        fields = "__all__"
