# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This serializer is responsible for serializing all
# medicine data. The medicine data is spread out over
# several tables in the database and therefore this
# serializer file has to access all different tables
# and merge all this data in an onedimensional object.
# ---------------------------------------------------

from rest_framework import serializers
from api.models.medicine_models import (
    Medicine,
    history_atc_code,
    history_authorisation_status,
    history_authorisation_type,
    history_brand_name,
    history_mah,
    history_number_check,
    history_od,
    history_prime,
)
from api.serializers.medicine_serializers.history_serializers import (
    ATCCodeSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    NumberCheckSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
)


# Creates medicine object per medicine
class PublicMedicineSerializer(serializers.ModelSerializer):
    """
    view endpoint medicine
    """

    atc_code = serializers.SerializerMethodField()
    authorisation_status = serializers.SerializerMethodField()
    authorisation_type = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    mah = serializers.SerializerMethodField()
    number_check = serializers.SerializerMethodField()
    orphan_designation = serializers.SerializerMethodField()
    prime = serializers.SerializerMethodField()

    class Meta:
        """
        Meta information
        """

        model = Medicine
        fields = "__all__"

    # retrieves atc code from database for each medicine
    def get_atc_code(self, atc_code):
        queryset = history_atc_code.objects.filter(eu_pnumber=atc_code.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return ATCCodeSerializer(instance=queryset, read_only=True).data

    # retrieves authorisation status from database for each medicine
    def get_authorisation_status(self, authorisation_status):
        queryset = history_authorisation_status.objects.filter(eu_pnumber=authorisation_status.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return AuthorisationStatusSerializer(instance=queryset, read_only=True).data

    # retrieves authorisation type from database for each medicine
    def get_authorisation_type(self, authorisation_type):
        queryset = history_authorisation_type.objects.filter(eu_pnumber=authorisation_type.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return AuthorisationTypeSerializer(instance=queryset, read_only=True).data

    # retrieves brand name from database for each medicine
    def get_brand_name(self, brand_name):
        queryset = history_brand_name.objects.filter(eu_pnumber=brand_name.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return BrandNameSerializer(instance=queryset, read_only=True).data

    # retrieves mah from database for each medicine
    def get_mah(self, mah):
        queryset = history_mah.objects.filter(eu_pnumber=mah.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return MAHSerializer(instance=queryset, read_only=True).data

    # retrieves number check from database for each medicine
    def get_number_check(self, number_check):
        queryset = history_number_check.objects.filter(eu_pnumber=number_check.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return NumberCheckSerializer(instance=queryset, read_only=True).data

    # retrieves orphan designation from database for each medicine
    def get_orphan_designation(self, orphan_designation):
        queryset = history_od.objects.filter(eu_pnumber=orphan_designation.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return OrphanDesignationSerializer(instance=queryset, read_only=True).data

    # retrieves primenumber from database for each medicine
    def get_prime(self, prime):
        queryset = history_prime.objects.filter(eu_pnumber=prime.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return PrimeSerializer(instance=queryset, read_only=True).data

    # creates one dimensional object from multiple dimensions
    def to_representation(self, obj):
        representation = super().to_representation(obj)

        for field in [
            "atc_code",
            "authorisation_status",
            "authorisation_type",
            "brand_name",
            "mah",
            "number_check",
            "orphan_designation",
            "prime",
        ]:
            field_representation = representation.pop(field)
            for key in field_representation:
                representation[key] = field_representation[key]

        return representation
