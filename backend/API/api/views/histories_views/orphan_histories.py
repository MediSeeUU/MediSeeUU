# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from .common import view_history
from api.models.orphan_models import (
    HistoryEUOrphanCon,
)
from api.serializers.medicine_serializers.histories.orphan_histories import (
    EUOrphanConSerializer,
)


class OrphanHistoriesViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request: Request, pk: str = None) -> Response:
        """
        Retrieve endpoint for the orphan history timeline

        Args:
            request (Request): The request being made by the user, not used
            pk (str): the eu_od_number being passed as url parameter

        Returns:
            Response: The orphan history timeline of the medicine with the specified eu_od_number
        """

        eu_od_number = pk.replace('_', '/')
        models_serializers = [
            (HistoryEUOrphanCon, EUOrphanConSerializer),
        ]
        user = self.request.user
        return Response(view_history(user, {"eu_od_number": eu_od_number}, models_serializers))

