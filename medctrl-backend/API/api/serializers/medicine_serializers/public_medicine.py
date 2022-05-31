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

#serialises authorization data
class AuthorisationSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = Authorisation
        exclude = ("eunumber",)

#serialises procudure data 
class ProcedureSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = Procedure
        fields = ("decisiondate",)

#serialises brandname data
class BrandnameSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = Historybrandname
        fields = ("brandname",)
        ordering = ("brandnamedate",)

#serialises MAH horization data
class MAHSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = Historymah
        fields = ("mah",)
        ordering = ("mahdate",)

#serialises orphan designation data
class OrphanSerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = Historyorphan
        fields = ("orphan",)
        ordering = ("orphandate",)

#serialises PRIME data
class PRIMESerializer(serializers.ModelSerializer):
    """
    Authorisation table serializer for the view endpoint medicine
    """

    class Meta:
        """
        Meta information
        """

        model = Historyprime
        fields = ("prime",)
        ordering = ("primedate",)

#Creates medicine object per medicine
class PublicMedicineSerializer(serializers.ModelSerializer):
    """
    view endpoint medicine
    """

    authorisation = serializers.SerializerMethodField()
    procedure = serializers.SerializerMethodField()
    brandname = serializers.SerializerMethodField()
    mah = serializers.SerializerMethodField()
    orphan = serializers.SerializerMethodField()
    prime = serializers.SerializerMethodField()

    class Meta:
        """
        Meta information
        """

        model = Medicine
        fields = "__all__"

    #retrieves authorization from data base for each medicie
    def get_authorisation(self, authorisation):
        queryset = Authorisation.objects.filter(eunumber=authorisation.eunumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return AuthorisationSerializer(instance=queryset, read_only=True).data

    #retrieves procedure from data base for each medicie
    def get_procedure(self, procedure):
        queryset = Procedure.objects.filter(
            procedurecount=1, eunumber=procedure.eunumber
        )
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return ProcedureSerializer(instance=queryset, read_only=True).data

    #retrieves brandname from data base for each medicie
    def get_brandname(self, brandname):
        queryset = Historybrandname.objects.filter(eunumber=brandname.eunumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return BrandnameSerializer(instance=queryset, read_only=True).data

    #retrieves mah from data base for each medicie
    def get_mah(self, mah):
        queryset = Historymah.objects.filter(eunumber=mah.eunumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return MAHSerializer(instance=queryset, read_only=True).data

    #retrieves orphan designation from data base for each medicie
    def get_orphan(self, orphan):
        queryset = Historyorphan.objects.filter(eunumber=orphan.eunumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return OrphanSerializer(instance=queryset, read_only=True).data

    #retrieves primenuber from data base for each medicie
    def get_prime(self, prime):
        queryset = Historyprime.objects.filter(eunumber=prime.eunumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return PRIMESerializer(instance=queryset, read_only=True).data

    #creates one dimensional object from multiple dimenssions
    def to_representation(self, obj):
        representation = super().to_representation(obj)

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

        return representation
