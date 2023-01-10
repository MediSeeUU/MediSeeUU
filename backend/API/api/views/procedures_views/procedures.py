# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from api.views.other import permission_filter
from api.models.human_models import (
    Procedures,
)
from api.serializers.medicine_serializers.public.human import (
    ProceduresSerializer,
)


class HumanHistoriesViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request: Request, pk: str = None) -> Response:
        eu_pnumber = pk.replace('_', '/')

        # retrieve data from database
        queryset = Procedures.objects.filter(eu_pnumber=eu_pnumber).all()
        serializer = ProceduresSerializer(queryset, many=True)
        procedures = serializer.data

        user = self.request.user
        perms = permission_filter(user)

        # filters medicines according to access level of the user
        filtered_procedures = map(
            lambda obj: {x: y for x, y in obj.items() if x in perms}, procedures
        )

        return Response(filtered_procedures)

