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
)
from api.update_cache import update_cache
from api.serializers.medicine_serializers.scraper import (
    MedicineSerializer,
    MedicineFlexVarUpdateSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
)
from datetime import date
from django.forms.models import model_to_dict
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
                # check if medicine already exists based on eunumber
                current_medicine = Medicine.objects.filter(
                    pk=medicine.get("eu_pnumber")
                ).first()
                # if exists update the medicine otherwise add it,
                # update works only on flexible variables
                logger.info("Van de medicine post request")
                logger.info("current medicine:")
                logger.info(current_medicine)

                if current_medicine:
                    errors = self.update_flex_medicine(medicine, current_medicine)
                    nullErrors = self.update_null_values(medicine)
                    if errors:
                        errors.extend(nullErrors)
                    else:
                        errors = nullErrors
                else:
                    errors = self.add_medicine(medicine, None)

                # if status is failed, add medicine to the failed list
                if errors and (len(errors) > 0):
                    medicine["errors"] = errors
                    failed_medicines.append(medicine)
            except Exception as e:
                medicine["errors"] = str(e)
                failed_medicines.append(medicine)

        update_cache()
        return Response(failed_medicines, status=200)

    def update_flex_medicine(self, data, current):
        """
        Update flexible medicine variables
        """

        medicine_serializer = MedicineFlexVarUpdateSerializer(current, data=data)

        history_variables(data)

        # update medicine
        if medicine_serializer.is_valid():
            medicine_serializer.save()
            return []
        return medicine_serializer.errors

    def add_medicine(self, data, current):
        """
        add medicine variables
        """

        # initialise serializers for addition
        serializer = MedicineSerializer(current, data=data)

        # add medicine and authorisation
        history_variables(data)
        if serializer.is_valid():
            serializer.save()
        else:
            return serializer.errors
        return []

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
            return self.add_medicine(new_data, current_medicine)


def history_variables(data):
    eu_pnumber = data.get("eu_pnumber")
    add_or_update_history(
        HistoryBrandName,
        BrandNameSerializer,
        "brandname",
        data.get("brandname"),
        data.get("change_date"),
        eu_pnumber,
    )
    add_or_update_history(
        HistoryMAH,
        MAHSerializer,
        "mah",
        data.get("mah"),
        data.get("change_date"),
        eu_pnumber,
    )
    # add_or_update_history(
    #     Historyorphan,
    #     OrphanSerializer,
    #     data.get("orphan"),
    #     "orphan",
    #     "orphandate",
    #     data.get("eunumber"),
    # )
    # add_or_update_history(
    #     Historyprime,
    #     PRIMESerializer,
    #     data.get("prime"),
    #     "prime",
    #     "primedate",
    #     data.get("eunumber"),
    # )


def add_or_update_history(model, serializer, name, item, date, eu_pnumber):
    if item is not None:
        model_data = (
            model.objects.filter(eu_pnumber=eu_pnumber).order_by("change_date").first()
        )
        if (not model_data) or item != getattr(model_data, name):
            serializer = serializer(
                None, {name: item, "change_date": date, "eu_pnumber": eu_pnumber}
            )
            if serializer.is_valid():
                serializer.save()
