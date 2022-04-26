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
