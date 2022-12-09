from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from api.models.human_models import models
import logging

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
        logging.getLogger(__name__).info(f"Anonymous group {get_action(created)}")

        # Create scraper user
        scraper, created = User.objects.update_or_create(username="scraper")
        logging.getLogger(__name__).info(f"Scraper user {get_action(created)}")

        # Assign permissions to scraper user
        for model in models:
            ct = ContentType.objects.filter(model=model.__name__).first()
            all_permissions = Permission.objects.filter(content_type=ct)
            scraper.user_permissions.add(*all_permissions)
