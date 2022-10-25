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
)
from api.update_cache import update_cache
from django.forms.models import model_to_dict
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class ScraperMedicine(APIView):
    """
    Class which provides an interface for the scraper to interact
    with the database models medicine and authorisation.
    """

    # Permission on this endpoint when user can add medicine
    permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        """
        Specify queryset for DjangoModelPermissions
        """
        return Medicine.objects.all()

    def post(self, request):
        """
        Post endpoint medicine scraper
        """
        # initialize list to return failed updates/adds, so these can be checked manually
        failed_medicines = []
        medicine_list = request.data.get("data")
        # get "medicine" key from request
        for medicine in medicine_list:
            try:
                # Atomic transaction so if there is any error all changes are rolled back
                # Django will automatically roll back if any exception occurs
                with transaction.atomic():
                    # check if medicine already exists based on eu_pnumber
                    current_medicine = Medicine.objects.filter(
                        pk=medicine.get("eu_pnumber")
                    ).first()
                    # if exists update the medicine otherwise add it,
                    # update works only on flexible variables

                    if current_medicine:
                        self.update_flex_medicine(medicine, current_medicine)
                        self.update_null_values(medicine)
                    else:
                        self.add_medicine(medicine, None)

            except Exception as e:
                medicine["errors"] = str(e)
                failed_medicines.append(medicine)
                logger.warning(f"Posted medicine failed to add to database: {medicine}")
            else:
                logger.info(f"Posted medicine successfully added to database: {medicine}")

        update_cache()
        return Response(failed_medicines, status=200)

    def update_flex_medicine(self, data, current):
        """
        Update flexible medicine variables
        """

        medicine_serializer = MedicineFlexVarUpdateSerializer(current, data=data, partial=True)

        # update medicine
        if medicine_serializer.is_valid():
            medicine_serializer.save()
            self.history_variables(data)
        else:
            raise ValueError(medicine_serializer.errors)

    def add_medicine(self, data, current):
        """
        add medicine variables
        """

        # initialise serializers for addition
        serializer = MedicineSerializer(current, data=data)

        # add medicine and authorisation
        if serializer.is_valid():
            serializer.save()
            self.history_variables(data)
        else:
            raise ValueError(serializer.errors)

    # Update only the values that are null for an existing medicine
    def update_null_values(self, data):
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

    # Create new history variables for the history models
    def history_variables(self, data):
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

    # Add new object to history model
    @staticmethod
    def add_history(model, serializer, name, data):
        eu_pnumber = data.get("eu_pnumber")
        item = data.get(name)
        model_data = model.objects.filter(eu_pnumber=eu_pnumber).order_by("change_date").first()

        if item is not None:
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
