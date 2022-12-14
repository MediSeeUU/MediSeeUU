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
from api.models import models
from api.models.human_models import (
    MedicinalProduct,
)
from .post_human import post as post_human
from .post_orphan import post as post_orphan
from api.views.update_cache import update_cache
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
        return MedicinalProduct.objects.all()

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
        if medicine_list:
            # get "medicine" key from request
            for medicine_data in medicine_list:
                try:
                    # atomic transaction so if there is any error all changes are rolled back
                    # Django will automatically roll back if any exception occurs
                    with transaction.atomic():
                        if medicine_data.get("orphan"):
                            post_orphan(medicine_data)
                        else:
                            post_human(medicine_data)
                except Exception as e:
                    medicine_data["errors"] = str(e)
                    failed_medicines.append(medicine_data)
                    logger.warning(f"Posted medicine failed to add to database: {medicine_data}")
                else:
                    logger.info(f"Posted medicine successfully added to database: {medicine_data}")

        # put all new medicine objects into the cache
        update_cache()
        # send back a list with all the failed medicines
        return Response(failed_medicines, status=200)
