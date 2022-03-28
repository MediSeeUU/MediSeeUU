from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Basic api config
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
