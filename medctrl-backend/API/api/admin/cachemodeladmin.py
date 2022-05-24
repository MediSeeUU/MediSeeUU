from django.contrib import admin
from api.update_cache import update_cache


class CacheModelAdmin(admin.ModelAdmin):
    """
    Admin View class.
    Every class that will inherit from this will automatically update the cache after data modifications.
    """

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        update_cache()

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        update_cache()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        update_cache()
