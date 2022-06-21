# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
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
