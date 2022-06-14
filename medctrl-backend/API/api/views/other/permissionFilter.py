# This file conatains the function that is used to fetch 
# the permissions apointed to an user.
#---------------------------------------------------------

from django.contrib.auth.models import Group

#Gets all permissions of a user
def permissionFilter(user):
    if user.is_anonymous:
        # If user is anonymous, return default permissions for anonymous group
        perms = Group.objects.get(name="anonymous").permissions.all()
        perms = [x.codename.split(".") for x in perms]
    else:
        perms = user.get_all_permissions(obj=None)
        perms = [x.split(".") for x in perms]

    perms = [x[-2] for x in perms if len(x) > 2 and x[-1] == "view"]
    return perms
