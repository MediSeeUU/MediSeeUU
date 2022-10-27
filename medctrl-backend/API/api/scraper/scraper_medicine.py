# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file can be accessed by the scraper via the medicine endpoint.
# When the scraper scrapes information about medicines, that data
# is posted to the medicine endpoint from where the data is
# processed in this file. If the new data is validated, it will
# be updated in the database.
# -------------------------------------------------------------

from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.medicine_models import (
    Medicine,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
    HistoryEUOrphanCon,
    LegalBases,
)
from api.serializers.medicine_serializers.scraper import (
    MedicineSerializer,
    MedicineFlexVarUpdateSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
    EUOrphanConSerializer,
    LegalBasesSerializer,
)
from api.update_cache import update_cache
from django.forms.models import model_to_dict
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class ScraperMedicine(APIView):
    """    
    The ScraperMedicine class provides an interface for the scraper to interact
    with the database models medicine and authorisation.

    Args:
        APIView (rest_framework.views.APIView): The current APIView from where communication handled
    """    

    # Permission on this endpoint when user can add medicine
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        """
        get_queryset specifies the queryset for DjangoModelPermissions. 
        DjangoModelPermissions is a list of medicine the user has permissions of.

        Returns:
            list[medicineObject]: Returns all medicine objects found in the medicine model.
        """
        return Medicine.objects.all()

    def post(self, request):
        """ 
        post is the post endpoint of this class. Medicine scraper communicates 
        via this endpoint to insert data into the database.

        Args:
            request (httpRequest): The data from the post request. This should contain a header
            with a valid token and a body with a json of medicine_data.

        Returns:
            httpResponse: Returns a list of all medicine that failed to get uploaded to the 
            database (failed_medicine) and status code 200.
        """
        # initialize list to return failed updates/adds, so these can be checked manually
        failed_medicines = []
        medicine_list = request.data.get("data")
        # get "medicine" key from request
        for medicine in medicine_list:
            try:
                # atomic transaction so if there is any error all changes are rolled back
                # Django will automatically roll back if any exception occurs
                with transaction.atomic():
                    # check if medicine already exists based on eu_pnumber
                    current_medicine = Medicine.objects.filter(
                        pk=medicine.get("eu_pnumber")
                    ).first()
                    # if the medicine doesn't exist or the medicine should be overriden, call add_medicine,
                    # otherwise update the flexible variables and the null values
                    override = medicine.get("override")
                    if current_medicine is None or override:
                        self.add_or_override_medicine(medicine, current_medicine, override)
                    else:
                        self.update_flex_medicine(medicine, current_medicine)
                        self.update_null_values(medicine)
            except Exception as e:
                medicine["errors"] = str(e)
                failed_medicines.append(medicine)
                logger.warning(f"Posted medicine failed to add to database: {medicine}")
            else:
                logger.info(f"Posted medicine successfully added to database: {medicine}")

        # put all new medicine objects into the cache
        update_cache()
        # send back a list with all the failed medicines
        return Response(failed_medicines, status=200)

    def update_flex_medicine(self, data, current):
        """
        This function updates the flexible medicine variables if this is applicable for the current data.
        The function is called if a previous version of the medicine already exists in the database.

        Args:
            data (medicineObject): The new medicine data.
            current (medicineObject): The medicine data that is currently in the database.
        """        
        medicine_serializer = MedicineFlexVarUpdateSerializer(current, data=data, partial=True)

        # update medicine
        if medicine_serializer.is_valid():
            medicine_serializer.save()
            self.history_variables(data)
            self.list_variables(data)
        else:
            raise ValueError(medicine_serializer.errors)

    def add_or_override_medicine(self, data, current, override: bool):
        """
        Adds a new medicine with its attributes to the database. If this is valid, 
        it will also add the history variables to the database.

        Args:
            data (medicineObject): The new medicine data.
            current (medicineObject): The medicine data that is currently in the database.
            override (bool): Specifies if the new medine should override an existing medicine.
        """        
        # initialise serializers for addition
        # partial is only allowed if an existing medicine is being overwritten
        serializer = MedicineSerializer(current, data=data, partial=current and override)

        # add medicine and authorisation
        if serializer.is_valid():
            serializer.save()
            self.history_variables(data)
            self.list_variables(data)
        else:
            raise ValueError(serializer.errors)

    def update_null_values(self, data):
        """
        Updates all null values for an existing medicine using the data given in its 
        argument "data".

        Args:
            data (medicineObject): The new medicine data.
        """        
        current_medicine = Medicine.objects.filter(pk=data.get("eu_pnumber")).first()

        medicine = model_to_dict(current_medicine)
        new_data = {"eu_pnumber": data.get("eu_pnumber")}

        for attr in medicine:
            if (getattr(current_medicine, attr) is None) and (
                    not (data.get(attr) is None)
            ):
                new_data[attr] = data.get(attr)

        if len(new_data.keys()) > 1:
            self.add_medicine(new_data, current_medicine)

    def list_variables(self, data):
        """
        Creates new list variables for the history models using the data given in its
        argument "data". It expects the input data to be formed like this:
        name: ["value1", "value2", ...]

        Args:
            data (medicineObject): The new medicine data.
        """
        self.add_list(
            LegalBases,
            LegalBasesSerializer,
            "eu_legal_basis",
            data,
            True,
        )

    @staticmethod
    def add_list(model, serializer, name, data, replace):
        """
        Add a new object to the given list model.

        Args:
            model (medicine_model): The list model of the list object you want to add.
            serializer (medicine_serializer): The applicable serializer.
            name (string): The name of the attribute.
            data (medicineObject): The new medicine data.
            replace (bool): If True, will delete all previously added objects with the same eu_pnumber

        Raises:
            ValueError: Invalid data in data argument
            ValueError: Data does not exist in the given data argument
        """
        eu_pnumber = data.get("eu_pnumber")
        items = data.get(name)
        model_data = model.objects.filter(eu_pnumber=eu_pnumber).all()

        if items is not None and len(items) > 0:
            for item in items:
                if model_data and replace:
                    model_data.delete()
                serializer = serializer(
                    None, {name: item, "eu_pnumber": eu_pnumber}
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(f"{name} contains invalid data! {serializer.errors}")
        elif not model_data:
            raise ValueError(f"{name} must be part of the data posted!")


    def history_variables(self, data):
        """
        Creates new history variables for the history models using the data given in its
        argument "data".

        Args:
            data (medicineObject): The new medicine data.
        """
        self.add_history(
            HistoryAuthorisationType,
            AuthorisationTypeSerializer,
            "eu_aut_type",
            data,
        )

        self.add_history(
            HistoryAuthorisationStatus,
            AuthorisationStatusSerializer,
            "eu_aut_status",
            data,
        )

        self.add_history(
            HistoryBrandName,
            BrandNameSerializer,
            "eu_brand_name",
            data,
        )

        self.add_history(
            HistoryOD,
            OrphanDesignationSerializer,
            "eu_od",
            data,
        )

        self.add_history(
            HistoryPrime,
            PrimeSerializer,
            "eu_prime",
            data,
        )

        self.add_history(
            HistoryMAH,
            MAHSerializer,
            "eu_mah",
            data,
        )

        self.add_history(
            HistoryEUOrphanCon,
            EUOrphanConSerializer,
            "eu_orphan_con",
            data,
        )

    @staticmethod
    def add_history(model, serializer, name, data):
        """
        Add a new object to the given history model.

        Args:
            model (medicine_model): The history model of the history object you want to add.
            serializer (medicine_serializer): The applicable serializer.
            name (string): The name of the attribute.
            data (medicineObject): The new medicine data.

        Raises:
            ValueError: Invalid data in data argument
            ValueError: Data does not exist in the given data argument
        """        
        eu_pnumber = data.get("eu_pnumber")
        items = data.get(name)
        model_data = model.objects.filter(eu_pnumber=eu_pnumber).order_by("change_date").first()

        if items is not None and len(items) > 0:
            for item in items:
                if not model_data or item.get(name) != getattr(model_data, name):
                    serializer = serializer(
                        None, {name: item.get(name), "change_date": item.get("change_date"), "eu_pnumber": eu_pnumber}
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValueError(f"{name} contains invalid data! {serializer.errors}")
        elif not model_data:
            raise ValueError(f"{name} must be part of the data posted!")
