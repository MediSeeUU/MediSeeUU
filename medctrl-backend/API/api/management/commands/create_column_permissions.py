from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from api.models.medicine_models import (
    Medicine,
    Authorisation,
    Procedure,
    Historyauthorisation,
    Historybrandname,
    Historyindication,
    Historymah,
    Historyprime,
    Historyorphan,
    Lookupactivesubstance,
    Lookupatccode,
    Lookuplegalbasis,
    Lookuplegalscope,
    Lookupmedicinetype,
    Lookupproceduretype,
    Lookuprapporteur,
    Lookupstatus,
)



class Command(BaseCommand):
    """
    Django admin command that creates permissions for all models in the API.
    """

    help = "Creates permissions for the columns per table"

    def handle(self, *args, **options):
        content_type = ContentType.objects.filter(model="medicine").first()

        for model in [
            Medicine,
            Authorisation,
            Procedure,
            Historyauthorisation,
            Historybrandname,
            Historyindication,
            Historymah,
            Historyprime,
            Historyorphan,
            Lookupactivesubstance,
            Lookupatccode,
            Lookuplegalbasis,
            Lookuplegalscope,
            Lookupmedicinetype,
            Lookupproceduretype,
            Lookuprapporteur,
            Lookupstatus,
        ]:
            content_type = ContentType.objects.filter(model=model.__name__).first()

            # pylint: disable=protected-access
            for field in model._meta.fields:
                if not field.is_relation:
                    name = f"{model.__name__.lower()}.{field.attname}.view"
                    description = f"Can view {field.name} in {model.__name__}"

                    perm, created = Permission.objects.update_or_create(
                        codename=name,
                        name=description,
                        content_type=content_type,
                    )
                    if created:
                        self.stdout.write(f"Created new permission '{perm}'")
                    else:
                        self.stdout.write(f"Permission '{perm}' already exists")
