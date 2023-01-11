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
    def handle(self, *args, **options):
        """
        Takes a username and password and creates a partner user. Partner users have permissions to change data in the database

        Args:

        """

        while not (username := input("Username: ")) or User.objects.filter(username=username).first():
            if username:
                self.stdout.write(self.style.NOTICE("Error: That username is already taken."))
            else:
                self.stdout.write(self.style.NOTICE("Error: This field cannot be blank."))

        password = password2 = None
        while password != password2 or not password:
            while not (password := getpass.getpass("Password: ")):
                self.stdout.write(self.style.NOTICE("Error: Blank passwords aren't allowed."))

            while not (password2 := getpass.getpass("Password (again): ")):
                self.stdout.write(self.style.NOTICE("Error: Blank passwords aren't allowed."))
            if password != password2:
                self.stdout.write(self.style.NOTICE("Error: Your passwords didn't match."))

        # Create user
        hash_password = make_password(password)
        partner_user = User.objects.create_user(username=username, password=hash_password)

        # Assign permissions to scraper user
        for model in models:
            ct = ContentType.objects.filter(model=model.__name__).first()
            all_permissions = Permission.objects.filter(content_type=ct)
            partner_user.user_permissions.add(*all_permissions)

        logging.getLogger(__name__).info(f"{username} partner user has been created")
        self.stdout.write(self.style.SUCCESS(f"Successfully created partner user \"{username}\""))
