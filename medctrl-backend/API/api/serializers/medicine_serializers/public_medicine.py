from rest_framework import serializers
from api.models.medicine_models import (
    Medicine,
    Authorisation,
    Procedure,
    Historybrandname,
    Historymah,
    Historyorphan,
    Historyprime,
)


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


class MAHSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historymah
        fields = ("mah",)
        ordering = ("mahdate",)


class OrphanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historyorphan
        fields = ("orphan",)
        ordering = ("orphandate",)


class PRIMESerializer(serializers.ModelSerializer):
    class Meta:
        model = Historyprime
        fields = ("prime",)
        ordering = ("primedate",)


class PublicMedicineSerializer(serializers.ModelSerializer):
    authorisation = serializers.SerializerMethodField()
    procedure = serializers.SerializerMethodField()
    brandname = serializers.SerializerMethodField()
    mah = serializers.SerializerMethodField()
    orphan = serializers.SerializerMethodField()
    prime = serializers.SerializerMethodField()

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

    def get_brandname(self, brandname):
        queryset = Historybrandname.objects.filter(eunumber=brandname.eunumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return BrandnameSerializer(instance=queryset, read_only=True).data

    def get_mah(self, mah):
        queryset = Historymah.objects.filter(eunumber=mah.eunumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return MAHSerializer(instance=queryset, read_only=True).data

    def get_orphan(self, orphan):
        queryset = Historyorphan.objects.filter(eunumber=orphan.eunumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return OrphanSerializer(instance=queryset, read_only=True).data

    def get_prime(self, prime):
        queryset = Historyprime.objects.filter(eunumber=prime.eunumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return PRIMESerializer(instance=queryset, read_only=True).data

    def to_representation(self, obj):
        representation = super().to_representation(obj)

        # Get the permissions that the user has from the requests' context
        #permissions = self.context.get("permissions")

        for field in [
            "authorisation",
            "procedure",
            "brandname",
            "mah",
            "orphan",
            "prime",
        ]:
            field_representation = representation.pop(field)
            for key in field_representation:
                representation[key] = field_representation[key]

        # Filter the representation to return only fields that the user has permission to view
        # representation_filtered = {
        #     x: y for x, y in representation.items() if x in permissions
        # }

        return representation
