from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import Group
from api.models import SavedSelection
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine
from rest_framework.response import Response
from django.core.cache import cache
from api.update_cache import update_cache


class MedicineViewSet(viewsets.ViewSet):
    """
    Viewset for the Medicine model
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # permissions.IsAuthenticated
    update_cache()

    def list(self, request):
        cache_medicine = cache.get("medicine_cache")

        # if the data is not present in the cache, we just obtain the data from the database
        if not cache_medicine:
            queryset = Medicine.objects.all()
            serializer = PublicMedicineSerializer(queryset, many=True)
            cache_medicine = serializer.data
        
        # selection = self.request.query_params.get("selection")

        # selection_set = SavedSelection.objects.filter(id=selection).first()
        # if selection_set is None:
        #     return Medicine.objects.none()

        # return selection_set.eunumbers.all()

        user = self.request.user
        if user.is_anonymous:
            # If user is anonymous, return default permissions for anonymous group
            perms = Group.objects.get(name="anonymous").permissions.all()
            perms = [x.codename.split(".") for x in perms]
        else:
            perms = user.get_all_permissions(obj=None)
            perms = [x.split(".") for x in perms]

        perms = [x[-2] for x in perms if len(x) > 2 and x[-1] == "view"]

        filtered_medicines = map(lambda obj : { x: y for x, y in obj.items() if x in perms }, cache_medicine)

        return Response(filtered_medicines)
