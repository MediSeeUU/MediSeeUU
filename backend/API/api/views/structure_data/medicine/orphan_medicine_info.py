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
from api.views.other.permissionFilter import permission_filter
from rest_framework import permissions
from api.models.create_dashboard_columns import Category


class OrphanMedicineInfo(views.APIView):
    """
    Viewset for the Medicine info
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, _):
        """
        Gathers all available information of orphan medicines with the current user's permissions
        and inserts it into a JSON. Each time a get request is send, this function is executed.

        Returns:
            JSON: The medicine information
        """
        user = self.request.user
        perm = permission_filter(user)
        return Response(get_medicine_info(perm, [Category.Orphan_product]))
