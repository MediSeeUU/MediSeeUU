from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password

from api.models.medicine_models import models
import logging

"""
This file is responsible for creating partner users. Partner users have permissions to change data in the database
"""

def get_action(created):
    """
    Returns the action that has been performed on the model
    """
    return "has been created" if created else "already exists"


def create_partner_user(username: str, password: str):
    """
    Takes a username and password and creates a partner user. Partner users have permissions to change data in the database

    Args:
        username (str): The username data of the corresponding user
        password (str): The password data of the corresponding user
    """

    # Create user
    hash_password = make_password(password)
    scraper, created = User.objects.update_or_create(username=username, password=hash_password)
    logging.getLogger(__name__).info(f"{username} user {get_action(created)}")

    # Assign permissions to scraper user
    for model in models:
        ct = ContentType.objects.filter(model=model.__name__).first()
        all_permissions = Permission.objects.filter(content_type=ct)
        scraper.user_permissions.add(*all_permissions)
