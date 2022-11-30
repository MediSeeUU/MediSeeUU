from django.db import models
from rest_framework import serializers
from typing import Tuple
from api.models import models as medicine_models
from api.models.create_dashboard_columns import DashboardRelatedColumn


def get_related_models(model: models.Model) -> list[Tuple[models.Model, serializers.ModelSerializer,
                                                          serializers.ModelSerializer]]:
    """

    Args:
        model:

    Returns:

    """
    result = []
    for medicine_model in medicine_models:
        for field in medicine_model._meta.get_fields():
            if hasattr(field, "dashboard_columns"):
                for dashboard_column in field.dashboard_columns:
                    if type(dashboard_column) == DashboardRelatedColumn:
                        if medicine_model == model or field.remote_field.model == model:
                            result.append((medicine_model, dashboard_column.public_serializer,
                                           dashboard_column.scraper_serializer))
    return result
