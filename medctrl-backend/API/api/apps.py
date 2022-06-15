# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Basic api config
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
