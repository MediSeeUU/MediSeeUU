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
    authorisation = AuthorisationSerializer()
    procedure = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = "__all__"
    
    def get_procedure(self, procedure):
        queryset = Procedure.objects.filter(procedurecount = 1, eunumber = procedure.eunumber)
        try:
          queryset = queryset[0]
        except:
          queryset = None
        return ProcedureSerializer(instance=queryset, read_only=True).data
    
    def to_representation(self, obj):
        representation = super().to_representation(obj)

        authorisation_representation = representation.pop('authorisation')
        for key in authorisation_representation:
            representation[key] = authorisation_representation[key]
        
        procedure_representation = representation.pop('procedure')
        for key in procedure_representation:
            representation[key] = procedure_representation[key]

        return representation
