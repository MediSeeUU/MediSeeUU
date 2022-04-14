from rest_framework import viewsets
from api.serializers.medicine_serializers import AtcCodeSerializer
from api.models.medicine_models import Lookupatccode


class AtcCodeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for atc code.
    """

    queryset = Lookupatccode.objects.all()
    serializer_class = AtcCodeSerializer
