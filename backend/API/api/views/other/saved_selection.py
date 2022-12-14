# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains all functions that are used for
# storing data selections of an authenticated users and
# fetching the data when necessary.
# --------------------------------------------------------

from rest_framework import viewsets
from api.serializers.other import SavedSelectionSerializer
from api.models.other import SavedSelection
from rest_framework import permissions, status
from rest_framework.response import Response


class SavedSelectionViewSet(viewsets.ModelViewSet):
    """
    Viewset for the SavedSelection model
    """

    serializer_class = SavedSelectionSerializer

    # Only users with correct permissions can create (or view) SavedSelections
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def create(self, request, *args, **kwargs):
        """
        Set the created_by to the requesting users' ID.

        Args:
            request (httpRequest): the incoming httpRequest
        """        
        request.data["created_by"] = request.user.id
        return super().create(request)

    def destroy(self, request, *args, **kwargs):  # Delete the SavedSelection
        """
        Deletes the SavedSelection.

        Args:
            request (httpRequest): the incoming httpRequest

        Returns:
            httpResponse: changes the status of the response.
        """        
        pk = kwargs.get("pk")
        obj = SavedSelection.objects.filter(created_by=request.user.id, id=pk).first()
        if obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """
        Fetches all stored data selections.
        
        Returns:
            JSON: A json with all user saved data.
        """        
        pk = self.kwargs.get("pk")

        if pk is None:
            return SavedSelection.objects.filter(created_by=self.request.user.id)

        return SavedSelection.objects.filter(id=pk)
