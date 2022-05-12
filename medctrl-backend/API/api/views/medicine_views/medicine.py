from rest_framework import viewsets
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine
from rest_framework import permissions
from api.serializers.user_serializers import UserSerializer
from django.contrib.auth.models import Group


class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    # Here we should make the distinction in access level --> change serializer based on access level

    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #permissions.IsAuthenticated
    serializer_class = PublicMedicineSerializer

    def get_queryset(self):
        serializer_class = UserSerializer
        user = self.request.user

        queryset = Medicine.objects.all()
        
        if user.is_anonymous:
            perm = Group.objects.get(name="anonymous").permissions.all()
            listt = [str(x) for x in perm]
            filteredSet = Medicine.objects.values(*listt)


        else:
            perm = user.get_all_permissions(obj=None)
            filteredSet = Medicine.objects.values(*perm)

        return filteredSet
