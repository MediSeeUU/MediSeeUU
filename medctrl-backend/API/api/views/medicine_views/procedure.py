from rest_framework import viewsets

from api.serializers.medicine_serializers import ProcedureSerializer
from api.models.medicine_models import Procedure

class ProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = ProcedureSerializer

    def get_queryset(self):
        eunumber = self.request.query_params.get('eunumber')
        return Procedure.objects.filter(eunumber = eunumber)
