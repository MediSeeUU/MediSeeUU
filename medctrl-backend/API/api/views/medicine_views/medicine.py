from rest_framework import viewsets
from rest_framework import permissions
from api.models.other import SavedSelection
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine
from rest_framework.response import Response
from django.core.cache import cache
from api.update_cache import update_cache
from api.views.other import permissionFilter

#Returns a list of mediciens acording to the acces level of the user
class MedicineViewSet(viewsets.ViewSet):
    """
    Viewset for the Medicine model
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
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

        #filters medicines acording to acces level of the user
        filtered_medicines = map(
            lambda obj: {x: y for x, y in obj.items() if x in perms}, cache_medicine
        )

        return Response(filtered_medicines)
