# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file is responsible for creating all custom
# permissions that are used in this project.
# ------------------------------------------------------

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from api.models import models
import logging


# creates custom permission levels to view medicines
class Command(BaseCommand):
    """
    Django admin command that creates permissions for all models in the API.
    """
    help = "Creates permissions for the columns per table"

    def handle(self, *args, **options):
        content_type = ContentType.objects.filter(model="medicine").first()

        for model in models:
            content_type = ContentType.objects.filter(model=model.__name__).first()

            # pylint: disable=protected-access
            for field in model._meta.get_fields():
                name = f"{model.__name__.lower()}.{field.name}.view"
                description = f"Can view {field.name} in {model.__name__}"

                columns = [(name, description)]

                # Add view permissions for every extra dashboard column
                if hasattr(field, "dashboard_columns"):
                    for dashboard_column in field.dashboard_columns:
                        data_key = dashboard_column.get_data_key(field.name)
                        if data_key != field.name:
                            name = f"{model.__name__.lower()}.{data_key}.view"
                            description = f"Can view {data_key} in {model.__name__}"
                            columns.append((name, description))

                for column in columns:
                    perm, created = Permission.objects.update_or_create(
                        codename=column[0],
                        name=column[1],
                        content_type=content_type,
                    )
                    if created:
                        logging.getLogger(__name__).info(f"Created new permission '{perm}'")
                    else:
                        logging.getLogger(__name__).info(f"Permission '{perm}' already exists")
