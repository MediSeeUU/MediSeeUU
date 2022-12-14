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
from api.models.orphan_models import models, OrphanProduct
from api.models.get_dashboard_columns import insert_extra_dashboard_columns
from api.serializers.medicine_serializers.public.orphan import OrphanProductSerializer
from api.views.other import permission_filter


class OrphanMedicineViewSet(viewsets.ViewSet):
    """
    View set for the Orphan model
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, _):
        """
        Returns a list of medicines according to the access level of the user

        Returns:
            httpResponse: returns a list of filtered medicine corresponding to this type of user.
        """
        orphan_cache = cache.get("orphan_cache")

        # if the data is not present in the cache, we just obtain the data from the database
        if not orphan_cache:
            queryset = OrphanProduct.objects.all()
            serializer = OrphanProductSerializer(queryset, many=True)
            data = serializer.data
            # Insert extra dashboard columns defined in the models
            orphan_cache = insert_extra_dashboard_columns(data, models)
            cache.set("orphan_cache", orphan_cache, None)

        user = self.request.user
        perms = permission_filter(user)

        # filters medicines according to access level of the user
        filtered_medicines = map(
            lambda obj: {x: y for x, y in obj.items() if x in perms}, orphan_cache
        )

        return Response(filtered_medicines)
