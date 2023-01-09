from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from api.models.human_models import models
from api.management.commands.create_partner_user import create_partner_user
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
        create_partner_user(username="scraper", password="VeranderDitWachtwoord123!")
