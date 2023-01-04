"""
| The human_models package contains all the orphan models for the backend.
| Django uses the models to create the database. Each models maps to a database table.
| The medicine models are used to store information about medicines received from the scraper
| and used to provide medicine information to the dashboard.
| Read more about models here: https://docs.djangoproject.com/en/4.1/topics/db/models/
"""
# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from .orphan_product import OrphanProduct
from .history_eu_orphan_con import HistoryEUOrphanCon

models = [
    OrphanProduct,
    HistoryEUOrphanCon,
]
