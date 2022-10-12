# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from .medicine_flex_var_update import MedicineFlexVarUpdateSerializer
from .public_medicine import PublicMedicineSerializer
from .medicine import MedicineSerializer
from .history_serializers import (
    ATCCodeSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    NumberCheckSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
)
from .public_history import (
    ATCCodeSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    NumberCheckSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
)

from .urls import UrlsSerializer