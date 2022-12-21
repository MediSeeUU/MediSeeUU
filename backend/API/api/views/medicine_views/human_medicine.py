# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all functions for the 'medicine view' endpoint.
# All data is fetched form the cache and filtered on the access level
# of the user.
# ------------------------------------------------------------------------------

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.core.cache import cache
from api.models.human_models import models, MedicinalProduct
from api.models.get_dashboard_columns import insert_extra_dashboard_columns
from api.serializers.medicine_serializers.public import PublicMedicinalProductSerializer
from api.views.update_cache import update_cache
from api.views.other import permission_filter
import logging

logger = logging.getLogger(__name__)


class HumanMedicineViewSet(viewsets.ViewSet):
    """
    View set for the Medicine model
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, _):
        """
        Returns a list of medicines according to the access level of the user

        Returns:
            httpResponse: returns a list of filtered medicine corresponding to this type of user.
        """        
        cache_medicine = cache.get("medicine_cache")

        # if the data is not present in the cache, we just obtain the data from the database
        if not cache_medicine:
            queryset = MedicinalProduct.objects.all()
            serializer = PublicMedicinalProductSerializer(queryset, many=True)
            cache_medicine = serializer.data
            cache.set("medicine_cache", cache_medicine, None)

        # Insert extra dashboard columns defined in the models
        data = insert_extra_dashboard_columns(cache_medicine, models)

        user = self.request.user
        perms = permission_filter(user)

        # filters medicines according to access level of the user
        filtered_medicines = map(
            lambda obj: {x: y for x, y in obj.items() if x in perms}, data
        )

        logger.info("Human medicines filtered on access level.")

        return Response(filtered_medicines)
