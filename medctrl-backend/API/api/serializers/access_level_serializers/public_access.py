from rest_framework import serializers
from api.models.medicine_models import Medicine
from api.models.medicine_models import Authorisation
from api.models.medicine_models import Procedure

class AuthorisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorisation
        exclude = ('eunumber', )

class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ('decisiondate', )

class MedicineSerializer(serializers.ModelSerializer):
    authorisation = AuthorisationSerializer(read_only=True)

    class Meta:
        model = Medicine
        fields = "__all__"
    
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        authorisation_representation = representation.pop('authorisation')
        for key in authorisation_representation:
            representation[key] = authorisation_representation[key]
        return representation
