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

# Returns a json file containing all information the detailed page and the filters need
class Medicine_info(views.APIView):
    """
    Viewset for the Medicine info
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # each time a get request is send, this function is executed.
    def get(self, request):
        user = self.request.user
        perm = permissionFilter(user)
        return Response(get_medicine_info(perm))
