from rest_framework import viewsets

from api.serializers.medicine_serializers import ProcedureSerializer
from api.models.medicine_models import Procedure

#returns procedures connected to each medicine
class ProcedureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for the Procedure model
    """

    serializer_class = ProcedureSerializer

    #gets a list of all procedures connected to each individual medicine
    def get_queryset(self):
        eunumber = self.kwargs["eunumber"]
        return Procedure.objects.filter(eunumber=eunumber)
