# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.core.cache import cache
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

    def retrieve(self, _, pk):
        pk = pk.replace('_', '/')

        human_histories_cache = cache.get("human_histories_cache_"+pk)

        if not human_histories_cache:
            human_histories_cache = []
            for model, serializer in [
                (HistoryAuthorisationStatus, AuthorisationStatusSerializer),
                (HistoryAuthorisationType, AuthorisationTypeSerializer),
                (HistoryBrandName, BrandNameSerializer),
                (HistoryEUOrphanCon, EUOrphanConSerializer),
                (HistoryMAH, MAHSerializer),
                (HistoryOD, OrphanDesignationSerializer),
                (HistoryPrime, PrimeSerializer),
            ]:
                queryset = model.objects.filter(eu_pnumber=pk).all()
                human_histories_cache.append(serializer(queryset, many=True).data)

            cache.set("human_histories_cache_"+pk, human_histories_cache, None)

        user = self.request.user
        perms = permission_filter(user)

        # filters medicines according to access level of the user
        #filtered_medicines = map(
        #   lambda obj: {x: y for x, y in obj.items() if x in perms}, human_histories_cache
        #)

        return Response(human_histories_cache)

