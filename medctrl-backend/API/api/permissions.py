# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from rest_framework import permissions


class CustomObjectPermissions(permissions.DjangoObjectPermissions):
    """
    Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
    """

    perms_map = {
        "GET": ["api.view_%(model_name)s"],
        "OPTIONS": ["api.view_%(model_name)s"],
        "HEAD": ["api.view_%(model_name)s"],
        "POST": ["api.add_%(model_name)s"],
        "PUT": ["api.change_%(model_name)s"],
        "PATCH": ["api.change_%(model_name)s"],
        "DELETE": ["api.delete_%(model_name)s"],
    }
