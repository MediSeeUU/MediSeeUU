# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from .common import view_history
from api.models.human_models import (
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
)
from api.serializers.medicine_serializers.histories.human_histories import (
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
)


class HumanHistoriesViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request: Request, pk: str = None) -> Response:
        """
        Retrieve endpoint for the human history timeline

        Args:
            request (Request): The request being made by the user, not used
            pk (str): the eu_pnumber being passed as url parameter

        Returns:
            Response: The human history timeline of the medicine with the specified eu_pnumber
        """

        eu_pnumber = pk.replace('_', '/')
        models_serializers = [
            (HistoryAuthorisationStatus, AuthorisationStatusSerializer, {"eu_pnumber": eu_pnumber}),
            (HistoryAuthorisationType, AuthorisationTypeSerializer, {"eu_pnumber": eu_pnumber}),
            (HistoryBrandName, BrandNameSerializer, {"eu_pnumber": eu_pnumber}),
            (HistoryMAH, MAHSerializer, {"eu_pnumber": eu_pnumber}),
            (HistoryOD, OrphanDesignationSerializer, {"eu_pnumber": eu_pnumber}),
            (HistoryPrime, PrimeSerializer, {"eu_pnumber": eu_pnumber}),
        ]
        user = self.request.user
        return Response(view_history(user, models_serializers))
