from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import Group
from api.models import SavedSelection
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine


class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    # Here we should make the distinction in access level --> change serializer based on access level

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]  # permissions.IsAuthenticated
    serializer_class = PublicMedicineSerializer

    def get_queryset(self):
        selection = self.request.query_params.get("selection")

        if selection is None:
            return Medicine.objects.all()

        selection_set = SavedSelection.objects.filter(id=selection).first()
        if selection_set is None:
            return Medicine.objects.none()

        return selection_set.eunumbers.all()

    def get_serializer_context(self):
        context = super(MedicineViewSet, self).get_serializer_context()

        user = self.request.user
        if user.is_anonymous:
            # If user is anonymous, return default permissions for anonymous group
            permissions = Group.objects.get(name="anonymous").permissions.all()
            permissions = [x.codename.split(".") for x in permissions]
        else:
            permissions = user.get_all_permissions(obj=None)
            permissions = [x.split(".") for x in permissions]

        permissions = [x[-2] for x in permissions if len(x) > 2 and x[-1] == "view"]

        # Set the permissions in the requests' context so the serializer can use them
        context.update({"permissions": permissions})

        return context
