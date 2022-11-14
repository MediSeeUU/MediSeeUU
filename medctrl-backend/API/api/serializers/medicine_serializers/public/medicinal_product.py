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
    MedicinalProduct,
    LegalBases,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
)
from api.serializers.medicine_serializers.public import (
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
)


class LegalBasesSerializer(serializers.ModelSerializer):
    """
    Legal bases table serializer for the view endpoint medicine
    """
    class Meta:
        """
        Meta information
        """
        model = LegalBases
        fields = ("eu_legal_basis",)


class PublicMedicineSerializer(serializers.ModelSerializer):
    """
    This is the view endpoint for a medicine.
    """
    eu_legal_basis = serializers.SerializerMethodField()
    eu_aut_status = serializers.SerializerMethodField()
    eu_aut_type_initial = serializers.SerializerMethodField()
    eu_aut_type_current = serializers.SerializerMethodField()
    eu_brand_name_initial = serializers.SerializerMethodField()
    eu_brand_name_current = serializers.SerializerMethodField()
    eu_mah_initial = serializers.SerializerMethodField()
    eu_mah_current = serializers.SerializerMethodField()
    eu_od_initial = serializers.SerializerMethodField()
    eu_prime_initial = serializers.SerializerMethodField()

    class Meta:
        """
        Meta information
        """
        model = MedicinalProduct
        fields = "__all__"

    def get_eu_legal_basis(self, legal_basis):
        """
        This retrieves the authorisation status from the database for each medicine.

        Args:
            legal_basis (Any): The legal basis of the medicine.

        Returns:
            str: Returns the data of the relevant serializer as JSON.
        """
        queryset = LegalBases.objects.filter(eu_pnumber=legal_basis.eu_pnumber)
        if len(queryset) == 0:
            queryset = None
        return LegalBasesSerializer(instance=queryset, read_only=True, many=True).data

    def get_eu_aut_status(self, authorisation_status):
        """
        This retrieves the authorisation status from the database for each medicine.

        Args:
            authorisation_status (Any): The autherisation status of the medicine.

        Returns:
            str: Returns the data of the relevant serializer as JSON.
        """        
        queryset = HistoryAuthorisationStatus.objects.filter(eu_pnumber=authorisation_status.eu_pnumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return AuthorisationStatusSerializer(instance=queryset, read_only=True).data


    def get_eu_aut_type_initial(self, authorisation_type):
        """
        This retrieves the initial authorisation type from the database for each medicine.

        Args:
            authorisation_type (Any): The autherisation status of the medicine.

        Returns:
            str: Returns the data of the relevant serializer as JSON.
        """        
        queryset = HistoryAuthorisationType.objects.filter(eu_pnumber=authorisation_type.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return AuthorisationTypeSerializer(instance=queryset, read_only=True).data


    def get_eu_aut_type_current(self, authorisation_type):
        """
        This retrieves the current authorisation type from the database for each medicine.

        Args:
            authorisation_type (Any): The autherisation type of the medicine.

        Returns:
            str: Returns the data of the relevant serializer as JSON.
        """   
        queryset = HistoryAuthorisationType.objects.filter(eu_pnumber=authorisation_type.eu_pnumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return AuthorisationTypeSerializer(instance=queryset, read_only=True).data


    def get_eu_brand_name_initial(self, brand_name):
        """
        This retrieves the initial brand name from the database for each medicine.

        Args:
            brand_name (Any): The brand name of the medicine.

        Returns:
            str: Returns the data of the relevant serializer as JSON.
        """   
        queryset = HistoryBrandName.objects.filter(eu_pnumber=brand_name.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return BrandNameSerializer(instance=queryset, read_only=True).data


    def get_eu_brand_name_current(self, brand_name):
        """
        This retrieves the current brand name from the database for each medicine.

        Args:
            brand_name (Any): The brand name of the medicine.

        Returns:
            str: Returns the data of the relevant serializer as JSON.
        """   
        queryset = HistoryBrandName.objects.filter(eu_pnumber=brand_name.eu_pnumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return BrandNameSerializer(instance=queryset, read_only=True).data


    def get_eu_mah_initial(self, mah):
        """
        This retrieves the initial marketing autherisation holder from the database for each medicine.

        Args:
            mah (Any): The marketing autherisation holder of the medicine.

        Returns:
            str: Returns the data of the relevant serializer as JSON.
        """   
        queryset = HistoryMAH.objects.filter(eu_pnumber=mah.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return MAHSerializer(instance=queryset, read_only=True).data


    def get_eu_mah_current(self, mah):
        """
        This retrieves the current marketing autherisation holder from the database for each medicine.

        Args:
            mah (Any): The marketing autherisation holder of the medicine.

        Returns:
            str: Returns the data of the relevant serializer as JSON.
        """   
        queryset = HistoryMAH.objects.filter(eu_pnumber=mah.eu_pnumber)
        try:
            queryset = queryset[0]
        except:
            queryset = None
        return MAHSerializer(instance=queryset, read_only=True).data


    def get_eu_od_initial(self, orphan_designation):
        """
        This retrieves the initial orphan designation from the database for each medicine.

        Args:
            orphan_designation (Any): The orphan designation of the medicine.

        Returns:
            str: Returns the data of the relevant serializer as JSON.
        """   
        queryset = HistoryOD.objects.filter(eu_pnumber=orphan_designation.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return OrphanDesignationSerializer(instance=queryset, read_only=True).data


    def get_eu_prime_initial(self, prime):
        """
        This retrieves the initial priority medicine designation from the database for each medicine.

        Args:
            prime (Any): The priority medicine designation of the medicine.

        Returns:
            str: Returns the data of the relevant serializer as JSON.
        """   
        queryset = HistoryPrime.objects.filter(eu_pnumber=prime.eu_pnumber)
        try:
            queryset = queryset[len(queryset) - 1]
        except:
            queryset = None
        return PrimeSerializer(instance=queryset, read_only=True).data

    def to_representation(self, obj):
        """
        This function creates a one-dimensional object from multiple fields.

        Args:
            obj (Any): Takes an object to be transformed.

        Returns:
            str: Returns a single JSON representation of the object.
        """        
        representation = super().to_representation(obj)

        # Change the representation for all history variables
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
        ]:
            field_representation = representation.pop(field)
            for key in field_representation:
                representation[field] = field_representation[key]

        # Change the representation for all list variables
        for field in [
            "eu_legal_basis",
        ]:
            field_representation = representation.pop(field)
            representation[field] = []
            for key in field_representation:
                for value in key.values():
                    representation[field].append(value)

        return representation
