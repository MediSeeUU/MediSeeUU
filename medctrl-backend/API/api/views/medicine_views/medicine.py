from rest_framework import viewsets
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine
from rest_framework import permissions
from api.serializers.user_serializers import UserSerializer
from django.contrib.auth.models import Group
from django.core.exceptions import FieldError
from rest_framework.response import Response
from django.core.cache import cache


class MedicineViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # permissions.IsAuthenticated
    queryset = Medicine.objects.all()
    serializer = PublicMedicineSerializer(queryset, many=True)
    cache.set("medicine_cache", serializer.data, None) # We set cache timeout to none so it never expires

    def list(self, request):
        cache_medicine = cache.get("medicine_cache")

        # if the data is not present in the cache, we just obtain the data from the database
        if not cache_medicine:
            queryset = Medicine.objects.all()
            serializer = PublicMedicineSerializer(queryset, many=True)
            cache_medicine = serializer.data

        user = self.request.user
        if user.is_anonymous:
            # If user is anonymous, return default permissions for anonymous group
            permA = Group.objects.get(name="anonymous").permissions.all()
            perm = [str(x.codename).split(".")[1] for x in permA if "." in x.codename]
        else:
            permB = user.get_all_permissions(obj=None)
            perm = [x.split(".")[2] for x in permB if "." in x]

        filtered_medicines = map(lambda obj : { x: y for x, y in obj.items() if x in perm }, cache_medicine)

        return Response(filtered_medicines)
