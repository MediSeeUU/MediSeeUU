# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)

# For each user all data is fetched from the database when opening
# the dashboard and stored in memory cache.
# This improves the performance of the GET requests by several seconds.
# -------------------------------------------------------------------

import io
from django.core.cache import cache
from django.core.management import call_command
from rest_framework.settings import settings

from api.serializers.medicine_serializers.public import PublicMedicineSerializer
from api.serializers.medicine_serializers.scraper import UrlsSerializer
from api.models.medicine_models import Medicine


# Adds all medicine data to cache memory of the server
def update_cache():
    if not settings.MEDICINES_CACHING:
        return

    if not has_pending_migrations() and not has_unapplied_migration():
        queryset = Medicine.objects.all()
        medicine_serializer = PublicMedicineSerializer(queryset, many=True)
        cache.set(
            "medicine_cache", medicine_serializer.data, None
        )  # We set cache timeout to none so it never expires
        urls_serializer = UrlsSerializer(queryset, many=True)
        cache.set(
            "urls_cache", urls_serializer.data, None
        )  # We set cache timeout to none so it never expires

    else:
        print("!!! There are pending migrations, skipping cache update !!!")


def has_pending_migrations():
    # Execute the makemigrations command and redirect its output to a StringIO object
    out = io.StringIO()
    call_command("makemigrations", dry_run=True, no_input=True, stdout=out)
    out.seek(0)
    result = out.read()
    return "No changes detected" not in result


def has_unapplied_migration():
    # Execute the showmigrations command and redirect its output to a StringIO object
    out = io.StringIO()
    call_command("showmigrations", list=True, no_color=True, stdout=out)
    out.seek(0)

    unapplied = [1 for line in out.readlines() if "[ ]" in line]

    return len(unapplied) > 0
