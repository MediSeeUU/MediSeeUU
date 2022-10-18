from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from api.models.medicine_models import (
    Medicine,
    HistoryATCCode,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
)

# This file is responsible for setting up some initial
# groups and users in the system.
# ------------------------------------------------------


def get_action(created):
    """
    Returns the action that has been performed on the model
    """
    return "has been created" if created else "already exists"


class Command(BaseCommand):
    """
    Django admin command that does the initial setup of the system.
    """

    help = "Initial MedCtrl setup"

    def handle(self, *args, **options):
        # Create anonymous group
        anon, created = Group.objects.update_or_create(name="anonymous")
        self.stdout.write(f"Anonymous group {get_action(created)}")

        # Create scraper user
        scraper, created = User.objects.update_or_create(username="scraper")
        self.stdout.write(f"Scraper user {get_action(created)}")

        # Assign permissions to scraper user
        for model in [
            Medicine,
            HistoryATCCode,
            HistoryAuthorisationStatus,
            HistoryAuthorisationType,
            HistoryBrandName,
            HistoryMAH,
            HistoryOD,
            HistoryPrime,
        ]:
            ct = ContentType.objects.filter(model=model.__name__).first()
            all_permissions = Permission.objects.filter(content_type=ct)
            scraper.user_permissions.add(*all_permissions)
