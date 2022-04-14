from rest_framework import viewsets
from api.serializers.medicine_serializers import AtcCodeSerializer
from api.models.medicine_models import AtcCode


class AtcCodeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions for atc code.
    """

    queryset = AtcCode.objects.all()
    serializer_class = AtcCodeSerializer
