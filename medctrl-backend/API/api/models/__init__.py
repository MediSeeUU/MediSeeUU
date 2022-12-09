"""
| The models package contains all the models for the backend.
| Django uses the models to create the database. Each models maps to a database table.
| The models are divided into a human_models package and an other package.
| Read more about models here: https://docs.djangoproject.com/en/4.1/topics/db/models/
"""
# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from .human_models import models as medicine_models
from .orphan_models import models as orphan_models
models = medicine_models + orphan_models
