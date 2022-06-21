# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from rest_framework import viewsets

from api.serializers.medicine_serializers import ProcedureSerializer
from api.models.medicine_models import Procedure


class ProcedureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for the Procedure model
    """

    serializer_class = ProcedureSerializer

    def get_queryset(self):
        eunumber = self.kwargs["eunumber"]
        return Procedure.objects.filter(eunumber=eunumber)
