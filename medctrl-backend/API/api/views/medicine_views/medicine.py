from rest_framework import viewsets
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine
from rest_framework import permissions
from api.serializers.user_serializers import UserSerializer
from django.contrib.auth.models import Group
from django.core.exceptions import FieldError
from rest_framework.response import Response


class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    # Here we should make the distinction in access level --> change serializer based on access level

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]  # permissions.IsAuthenticated
    serializer_class = PublicMedicineSerializer

    def get_queryset(self):
        serializer_class = UserSerializer

        queryset = Medicine.objects.all()
        return queryset

    def get_serializer_context(self):
        context = super(MedicineViewSet, self).get_serializer_context()

        user = self.request.user
        if user.is_anonymous:
            # If user is anonymous, return default permissions for anonymous group
            permA = Group.objects.get(name="anonymous").permissions.all()
            perm = [str(x.codename).split(".")[1] for x in permA if "." in x.codename]
        else:
            permB = user.get_all_permissions(obj=None)
            perm = [x.split(".")[2] for x in permB if "." in x]

        # Set the permissions in the requests' context so the serializer can use them
        context.update({"permissions": perm})

        return context
