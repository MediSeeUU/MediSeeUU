# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all functions for the 'medicine view' endpoint.
# All data is fetched form the cache and filtered on the access level
# of the user.
# ------------------------------------------------------------------------------

from rest_framework import viewsets
from rest_framework import permissions
from api.serializers.medicine_serializers.public import OrphanProductSerializer
from api.models.orphan_models import OrphanProduct
from rest_framework.response import Response
from django.core.cache import cache
from api.views.update_cache import update_cache
from api.views.other import permission_filter
import logging

logger = logging.getLogger(__name__)


class OrphanMedicineViewSet(viewsets.ViewSet):
    """
    View set for the Orphan model
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    update_cache()

    def list(self, _):
        """
        Returns a list of medicines according to the access level of the user

        Returns:
            httpResponse: returns a list of filtered medicine corresponding to this type of user.
        """
        cache_medicine = cache.get("orphan_cache")

        # if the data is not present in the cache, we just obtain the data from the database
        if not cache_medicine:
            queryset = OrphanProduct.objects.all()
            serializer = OrphanProductSerializer(queryset, many=True)
            cache_medicine = serializer.data
            cache.set("orphan_cache", cache_medicine, None)

        user = self.request.user
        perms = permission_filter(user)

        # filters medicines according to access level of the user
        filtered_medicines = map(
            lambda obj: {x: y for x, y in obj.items() if x in perms}, cache_medicine
        )

        logger.info("Orphan medicines filtered on access level.")

        return Response(filtered_medicines)