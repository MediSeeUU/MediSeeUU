"""
| The admin package defines admin views for the models, which can be used in Django's admin panel.
| Read more about the admin site here: https://docs.djangoproject.com/en/4.1/ref/contrib/admin/
"""
# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from .common import CustomForeignKeyWidget, import_foreign_key
from .cachemodeladmin import CacheModelAdmin

# importing all admin models
from .history_authorisation_status_admin import HistoryAuthorisationStatusResource, HistoryAuthorisationStatusAdmin
from .history_authorisation_type_admin import HistoryAuthorisationTypeResource, HistoryAuthorisationTypeAdmin
from .history_brand_name_admin import HistoryBrandNameResource, HistoryBrandNameAdmin
from .history_eu_orphan_con_admin import HistoryEUOrphanConResource, HistoryEUOrphanConAdmin
from .history_mah_admin import HistoryMAHResource, HistoryMAHAdmin
from .history_od_admin import HistoryODResource, HistoryODAdmin
from .history_prime_admin import HistoryPrimeResource, HistoryPrimeAdmin
from .medicine_admin import MedicineResource, MedicineAdmin