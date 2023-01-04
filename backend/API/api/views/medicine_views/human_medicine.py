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
from api.serializers.medicine_serializers.public.human import PublicMedicinalProductSerializer
from api.views.other import permission_filter


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
        human_cache = cache.get("human_cache")

        # if the data is not present in the cache, we just obtain the data from the database
        if not human_cache:
            queryset = MedicinalProduct.objects.all()
            serializer = PublicMedicinalProductSerializer(queryset, many=True)
            data = serializer.data
            # Insert extra dashboard columns defined in the models
            human_cache = insert_extra_dashboard_columns(data, models)
            cache.set("human_cache", human_cache, None)

        user = self.request.user
        perms = permission_filter(user)

        # filters medicines according to access level of the user
        filtered_medicines = map(
            lambda obj: {x: y for x, y in obj.items() if x in perms}, human_cache
        )

        return Response(filtered_medicines)
