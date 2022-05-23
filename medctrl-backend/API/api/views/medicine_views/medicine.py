from rest_framework import viewsets
from rest_framework import permissions
from api.models import SavedSelection
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine
from rest_framework.response import Response
from django.core.cache import cache
from api.update_cache import update_cache
from api.views.other import permissionFilter


class MedicineViewSet(viewsets.ViewSet):
    """
    Viewset for the Medicine model
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]  # permissions.IsAuthenticated
    update_cache()

    def list(self, request):
        cache_medicine = cache.get("medicine_cache")

        # if the data is not present in the cache, we just obtain the data from the database
        if not cache_medicine:
            queryset = Medicine.objects.all()
            serializer = PublicMedicineSerializer(queryset, many=True)
            cache_medicine = serializer.data

        user = self.request.user
        perms = permissionFilter(user)

        filtered_medicines = map(
            lambda obj: {x: y for x, y in obj.items() if x in perms}, cache_medicine
        )

        return Response(filtered_medicines)
