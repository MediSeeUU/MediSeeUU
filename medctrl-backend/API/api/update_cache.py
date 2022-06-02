import io
from django.core.cache import cache
from django.core.management import call_command
from rest_framework.settings import settings

from api.serializers.medicine_serializers import PublicMedicineSerializer
from api.models.medicine_models import Medicine


def update_cache():
    if not settings.MEDICINES_CACHING:
        return

    if not has_pending_migrations():
        queryset = Medicine.objects.all()
        serializer = PublicMedicineSerializer(queryset, many=True)
        cache.set(
            "medicine_cache", serializer.data, None
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
