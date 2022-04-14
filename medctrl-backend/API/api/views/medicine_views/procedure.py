from rest_framework import viewsets
from api.serializers.medicine_serializers import ProcedureSerializer
from api.models.medicine_models import Procedure


class ProcedureViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for atc code.
    """

    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
