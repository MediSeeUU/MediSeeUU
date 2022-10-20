# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# This file is responsible for creating all custom
# permissions that are used in this project.
# ------------------------------------------------------

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from api.models.medicine_models import (
    Medicine,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
)

# creates custom permission levels to view medicines
class Command(BaseCommand):
    """
    Django admin command that creates permissions for all models in the API.
    """

    help = "Creates permissions for the columns per table"

    def handle(self, *args, **options):
        content_type = ContentType.objects.filter(model="medicine").first()

        for model in [
            Medicine,
            HistoryAuthorisationStatus,
            HistoryAuthorisationType,
            HistoryBrandName,
            HistoryMAH,
            HistoryOD,
            HistoryPrime,
        ]:
            content_type = ContentType.objects.filter(model=model.__name__).first()

            # pylint: disable=protected-access
            for field in model._meta.get_fields():
                name = f"{model.__name__.lower()}.{field.name}.view"
                description = f"Can view {field.name} in {model.__name__}"

                columns = [(name, description)]

                # Add view permissions for every extra dashboard column
                if hasattr(field, "dashboard_columns"):
                    for dashboard_column in field.dashboard_columns:
                        if dashboard_column.data_key is not field.name:
                            name = f"{model.__name__.lower()}.{dashboard_column.data_key}.view"
                            description = f"Can view {dashboard_column.data_key} in {model.__name__}"
                            columns.append((name, description))

                for column in columns:
                    perm, created = Permission.objects.update_or_create(
                        codename=column[0],
                        name=column[1],
                        content_type=content_type,
                    )
                    if created:
                        self.stdout.write(f"Created new permission '{perm}'")
                    else:
                        self.stdout.write(f"Permission '{perm}' already exists")