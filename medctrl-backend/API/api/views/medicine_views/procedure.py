from rest_framework import viewsets
from rest_framework_guardian import filters

from api.permissions import CustomObjectPermissions
from api.serializers.medicine_serializers import ProcedureSerializer
from api.models.medicine_models import Procedure

class ProcedureViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for atc code.
    """

    permission_classes = [CustomObjectPermissions]
    filter_backends = [filters.ObjectPermissionsFilter]

    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
