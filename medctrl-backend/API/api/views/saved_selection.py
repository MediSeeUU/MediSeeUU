from rest_framework import viewsets
from api.permissions import CustomObjectPermissions
from api.serializers import SavedSelectionSerializer
from api.models import SavedSelection
from rest_framework import permissions


class SavedSelectionViewSet(viewsets.ModelViewSet):
    """
    Viewset for the SavedSelection model
    """

    serializer_class = SavedSelectionSerializer

    # Only users with correct permissions can create (or view) SavedSelections
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def create(self, request, *args, **kwargs):
        # set the created_by to the requesting users' ID
        request.data["created_by"] = request.user.id
        return super().create(request)

    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if pk is None:
            return SavedSelection.objects.filter(created_by=self.request.user.id)

        return SavedSelection.objects.filter(id=pk)
