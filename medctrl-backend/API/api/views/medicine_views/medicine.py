from rest_framework import viewsets
from rest_framework import permissions
from api.models import SavedSelection
from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine
from api.views.other import permissionFilter


class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for the Medicine model
    """

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
        context = super().get_serializer_context()

        user = self.request.user
        perms = permissionFilter(user)

        # Set the permissions in the requests' context so the serializer can use them
        context.update({"permissions": perms})

        return context
