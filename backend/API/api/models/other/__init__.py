"""
| The other package contains all the models  for the backend which don't contain medicine information.
| Django uses the models to create the database. Each models maps to a database table.
| Read more about models here: https://docs.djangoproject.com/en/4.1/topics/db/models/
"""
# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from .locks import Locks, LockModel
