from rest_framework import views
from rest_framework.response import Response
from .medicine_info_json import get_medicine_info
from .permissionFilter import permissionFilter
from rest_framework import permissions


class Medicine_info(views.APIView):
    """
    Viewset for the Medicine info
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]  # permissions.IsAuthenticated

    def get(self, request):
        user = self.request.user
        perm = permissionFilter(user)
        return Response(get_medicine_info(perm))
