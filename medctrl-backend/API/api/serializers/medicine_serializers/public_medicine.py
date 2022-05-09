from rest_framework import serializers
from api.models.medicine_models import Medicine, Authorisation, Procedure, Historybrandname


class AuthorisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorisation
        exclude = ("eunumber",)


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ("decisiondate",)


class BrandnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historybrandname
        fields = ("brandname",)
        ordering = ("brandnamedate",)


class PublicMedicineSerializer(serializers.ModelSerializer):
    authorisation = serializers.SerializerMethodField()
    procedure = serializers.SerializerMethodField()
    brandname = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = "__all__"

    def get_authorisation(self, authorisation):
        queryset = Authorisation.objects.filter(eunumber=authorisation.eunumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return AuthorisationSerializer(instance=queryset, read_only=True).data

    def get_procedure(self, procedure):
        queryset = Procedure.objects.filter(
            procedurecount=1, eunumber=procedure.eunumber
        )
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return ProcedureSerializer(instance=queryset, read_only=True).data


    def to_representation(self, obj):
        representation = super().to_representation(obj)
        for field in ["authorisation", "procedure"]:
            field_representation = representation.pop(field)
            for key in field_representation:
                representation[key] = field_representation[key]
        return representation
