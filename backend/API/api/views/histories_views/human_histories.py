# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from api.views.other import permission_filter
from api.models.human_models import (
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryEUOrphanCon,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
)
from api.serializers.medicine_serializers.histories import (
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    EUOrphanConSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
)


class HumanHistoriesViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, _, pk=None):
        eu_pnumber = pk.replace('_', '/')

        human_histories = []
        for model, serializer in [
            (HistoryAuthorisationStatus, AuthorisationStatusSerializer),
            (HistoryAuthorisationType, AuthorisationTypeSerializer),
            (HistoryBrandName, BrandNameSerializer),
            (HistoryEUOrphanCon, EUOrphanConSerializer),
            (HistoryMAH, MAHSerializer),
            (HistoryOD, OrphanDesignationSerializer),
            (HistoryPrime, PrimeSerializer),
        ]:
            queryset = model.objects.filter(eu_pnumber=eu_pnumber).all()
            human_histories.append(serializer(queryset, many=True).data)

        user = self.request.user
        perms = permission_filter(user)

        # Concat all histories
        human_histories = [inner for outer in human_histories for inner in outer]

        # Sort by change_date, ascending
        human_histories = sorted(human_histories, key=lambda d: d["change_date"])

        # filters histories according to access level of the user
        filtered_histories = [history for history in human_histories if all(key in perms for key in history.keys())]

        return Response(filtered_histories)
