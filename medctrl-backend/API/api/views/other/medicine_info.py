# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file contains the view for the endpoint that
# is concerned with additional information about all
# fields in the database.
# ---------------------------------------------------------

from rest_framework import views
from rest_framework.response import Response
from .medicine_info_json import get_medicine_info
from .permissionFilter import permissionFilter
from rest_framework import permissions


class Medicine_info(views.APIView):
    """
    Viewset for the Medicine info
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        """
        Gathers all available information with the current user's permissions 
        and inserts it into a JSON. Each time a get request is send, this 
        function is executed.

        Args:
            request (httpRequest): the incoming httpRequest

        Returns:
            JSON: The medicine information
        """        
        user = self.request.user
        perm = permissionFilter(user)
        return Response(get_medicine_info(perm))
