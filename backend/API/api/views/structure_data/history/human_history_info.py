# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import views
from rest_framework.response import Response
from .history_info_json import get_history_info
from api.views.other.permissionFilter import permission_filter
from rest_framework import permissions
from api.models.human_models import models


class HumanHistoryInfo(views.APIView):
    """
    Viewset for the human history info
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, _):
        """
        Gathers all available information of human medicines with the current user's permissions
        and inserts it into a JSON. Each time a get request is send, this function is executed.

        Returns:
            JSON: The medicine information
        """
        user = self.request.user
        perm = permission_filter(user)
        return Response(get_history_info(perm, models))
