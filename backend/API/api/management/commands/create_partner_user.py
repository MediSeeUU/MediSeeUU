# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from api.models import models
import logging
import getpass

"""
This file is responsible for creating partner users. Partner users have permissions to change data in the database
"""


class Command(BaseCommand):

    def get_action(self, created):
        """
        Returns the action that has been performed on the model
        """
        return "has been created" if created else "already exists"

    def handle(self, *args, **options):
        """
        Takes a username and password and creates a partner user. Partner users have permissions to change data in the database

        Args:

        """

        while not (username := input("Enter a username: ")) or User.objects.filter(username=username).first():
            if username:
                self.stdout.write(self.style.NOTICE("Username already exists"))
            else:
                self.stdout.write(self.style.NOTICE("Please enter a valid username"))

        while not (password := getpass.getpass("Enter a password: ")):
            self.stdout.write(self.style.NOTICE("Please enter a valid password"))

        # Create user
        hash_password = make_password(password)
        partner_user = User.objects.create_user(username=username, password=hash_password)

        # Assign permissions to scraper user
        for model in models:
            ct = ContentType.objects.filter(model=model.__name__).first()
            all_permissions = Permission.objects.filter(content_type=ct)
            partner_user.user_permissions.add(*all_permissions)

        logging.getLogger(__name__).info(f"{username} user has been created")
        self.stdout.write(self.style.SUCCESS('Successfully created partner user "%s"' % username))
