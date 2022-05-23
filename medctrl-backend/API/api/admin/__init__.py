from .common import CustomForeignKeyWidget, import_foreign_key
from .medicineadmin import MedicineResource, MedicineAdmin
from .authorisationadmin import AuthorisationResource, AuthorisationAdmin
from .procedureadmin import ProcedureResource, ProcedureAdmin
from .historyauthorisationadmin import (
    HistoryauthorisationResource,
    HistoryauthorisationAdmin,
)
from .historybrandnameadmin import HistorybrandnameResource, HistorybrandnameAdmin
from .historyindication import HistoryindicationResource, HistoryindicationAdmin
from .historymahadmin import HistorymahResource, HistorymahAdmin
from .historyorphanadmin import HistoryorphanResource, HistoryorphanAdmin
from .historyprimeadmin import HistoryprimeResource, HistoryprimeAdmin
from .cachemodeladmin import CacheModelAdmin
