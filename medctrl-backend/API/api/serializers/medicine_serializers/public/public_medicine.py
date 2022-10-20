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
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
    HistoryEUOrphanCon
)
from api.serializers.medicine_serializers.public import (
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
    EUOrphanConSerializer
)


# Creates medicine object per medicine
class PublicMedicineSerializer(serializers.ModelSerializer):
    """
    view endpoint medicine
    """

    eu_aut_status = serializers.SerializerMethodField()
    eu_aut_type_initial = serializers.SerializerMethodField()
    eu_aut_type_current = serializers.SerializerMethodField()
    eu_brand_name_initial = serializers.SerializerMethodField()
    eu_brand_name_current = serializers.SerializerMethodField()
    eu_mah_initial = serializers.SerializerMethodField()
    eu_mah_current = serializers.SerializerMethodField()
    eu_od_initial = serializers.SerializerMethodField()
    eu_prime_initial = serializers.SerializerMethodField()
    eu_orphan_con_initial = serializers.SerializerMethodField()
    eu_orphan_con_current = serializers.SerializerMethodField()

    class Meta:
        """
        Meta information
        """

        model = Medicine
        fields = "__all__"

    # retrieves authorisation status from database for each medicine
    def get_eu_aut_status(self, authorisation_status):
        queryset = HistoryAuthorisationStatus.objects.filter(eu_pnumber=authorisation_status.eu_pnumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return AuthorisationStatusSerializer(instance=queryset, read_only=True).data

    # retrieves initial authorisation type from database for each medicine
    def get_eu_aut_type_initial(self, authorisation_type):
        queryset = HistoryAuthorisationType.objects.filter(eu_pnumber=authorisation_type.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return AuthorisationTypeSerializer(instance=queryset, read_only=True).data


    # retrieves authorisation type from database for each medicine
    def get_eu_aut_type_current(self, authorisation_type):
        queryset = HistoryAuthorisationType.objects.filter(eu_pnumber=authorisation_type.eu_pnumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return AuthorisationTypeSerializer(instance=queryset, read_only=True).data

    # retrieves initial brand name from database for each medicine
    def get_eu_brand_name_initial(self, brand_name):
        queryset = HistoryBrandName.objects.filter(eu_pnumber=brand_name.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return BrandNameSerializer(instance=queryset, read_only=True).data

    # retrieves current brand name from database for each medicine
    def get_eu_brand_name_current(self, brand_name):
        queryset = HistoryBrandName.objects.filter(eu_pnumber=brand_name.eu_pnumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return BrandNameSerializer(instance=queryset, read_only=True).data


    # retrieves initial mah from database for each medicine
    def get_eu_mah_initial(self, mah):
        queryset = HistoryMAH.objects.filter(eu_pnumber=mah.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return MAHSerializer(instance=queryset, read_only=True).data

    # retrieves current mah from database for each medicine
    def get_eu_mah_current(self, mah):
        queryset = HistoryMAH.objects.filter(eu_pnumber=mah.eu_pnumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return MAHSerializer(instance=queryset, read_only=True).data


    # retrieves initial orphan designation from database for each medicine
    def get_eu_od_initial(self, orphan_designation):
        queryset = HistoryOD.objects.filter(eu_pnumber=orphan_designation.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return OrphanDesignationSerializer(instance=queryset, read_only=True).data

    # retrieves initial primenumber from database for each medicine
    def get_eu_prime_initial(self, prime):
        queryset = HistoryPrime.objects.filter(eu_pnumber=prime.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return PrimeSerializer(instance=queryset, read_only=True).data

    # retrieves initial orphan conditions from database for each medicine
    def get_eu_orphan_con_initial(self, orphan_con):
        queryset = HistoryEUOrphanCon.objects.filter(eu_pnumber=orphan_con.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return EUOrphanConSerializer(instance=queryset, read_only=True).data

    # retrieves current orphan conditions from database for each medicine
    def get_eu_orphan_con_current(self, orphan_con):
        queryset = HistoryEUOrphanCon.objects.filter(eu_pnumber=orphan_con.eu_pnumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return EUOrphanConSerializer(instance=queryset, read_only=True).data


    # creates one dimensional object from multiple dimensions
    def to_representation(self, obj):
        representation = super().to_representation(obj)

        for field in [
            "eu_aut_status",
            "eu_aut_type_initial",
            "eu_aut_type_current",
            "eu_brand_name_initial",
            "eu_brand_name_current",
            "eu_mah_initial",
            "eu_mah_current",
            "eu_od_initial",
            "eu_prime_initial",
            "eu_orphan_con_initial",
            "eu_orphan_con_current",
        ]:
            field_representation = representation.pop(field)
            for key in field_representation:
                representation[field] = field_representation[key]

        return representation
