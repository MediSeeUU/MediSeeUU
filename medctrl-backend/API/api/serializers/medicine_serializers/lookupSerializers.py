from rest_framework import serializers
from api.models.medicine_models import Lookupactivesubstance, Lookupatccode, Lookuplegalbasis, Lookuplegalscope, Lookupmedicinetype, Lookupstatus, Lookuprapporteur

class LookupActiveSubstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookupactivesubstance
        fields = "__all__"

class LookupAtccodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookupatccode
        fields = "__all__"

class LookupLegalbasisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookuplegalbasis
        fields = "__all__"

class LookupLegalscopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookuplegalscope
        fields = "__all__"

class LookupMedicinetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookupmedicinetype
        fields = "__all__"

class LookupStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookupstatus
        fields = "__all__"

class LookupRapporteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookuprapporteur
        fields = "__all__"