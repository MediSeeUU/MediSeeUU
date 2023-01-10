# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
from django.contrib import admin
from import_export import resources, admin as import_admin
from api.models.other import Locks
from api.admin.common import import_foreign_key
from api.admin.cachemodeladmin import CacheModelAdmin


class LocksResource(resources.ModelResource):
    """
    Necessary resource class for the Locks admin view.
    ModelResource is Resource subclass for handling Django models.
    """

    class Meta:
        """
        Meta class for LocksResource
        """
        model = Locks


class LocksAdmin(import_admin.ImportExportModelAdmin, admin.ModelAdmin):
    """
    Admin View for Locks
    """
    resource_class = LocksResource
    list_display = [
        "model_name",
        "model_pk",
        "column_name",
    ]


admin.site.register(Locks, LocksAdmin)
