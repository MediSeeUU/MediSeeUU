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
    history_atc_code,
    history_authorisation_status,
    history_authorisation_type,
    history_brand_name,
    history_mah,
    history_number_check,
    history_od,
    history_prime,
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
            history_atc_code,
            history_authorisation_status,
            history_authorisation_type,
            history_brand_name,
            history_mah,
            history_number_check,
            history_od,
            history_prime,
        ]:
            content_type = ContentType.objects.filter(model=model.__name__).first()

            # pylint: disable=protected-access
            for field in model._meta.fields:
                name = f"{model.__name__.lower()}.{field.name}.view"
                description = f"Can view {field.name} in {model.__name__}"

                perm, created = Permission.objects.update_or_create(
                    codename=name,
                    name=description,
                    content_type=content_type,
                )
                if created:
                    self.stdout.write(f"Created new permission '{perm}'")
                else:
                    self.stdout.write(f"Permission '{perm}' already exists")