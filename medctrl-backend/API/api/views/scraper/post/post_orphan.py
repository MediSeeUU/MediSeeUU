from django.forms.models import model_to_dict
from api.models.orphan_models import (
    OrphanProduct,
)
from api.serializers.medicine_serializers.scraper.post.orphan import (
    OrphanProductSerializer,
)
from api.models.other import OrphanLocks


def post(data):
    if eu_od_number := data.get("eu_od_number"):
        locks = OrphanLocks.objects.filter(
            eu_od_number=eu_od_number
        ).values_list("column_name", flat=True)

        data = {key: value for key, value in data.items() if key not in locks}


def orphan_history_variables(data):
    """
    Creates new history variables for the orphan product history models using the data given in its
    argument "data". It expects the input data for the history variable to be formed like this:
    ``name: [{name: value, change_date: date}, ...]``

    Args:
        data (medicineObject): The new medicine data.
    """
    pass


def add_orphan_history(model, serializer, name, data):
    """
    Add a new object to the given history model.

    Args:
        model (medicine_model): The history model of the history object you want to add.
        serializer (medicine_serializer): The applicable serializer.
        name (string): The name of the attribute.
        data (medicineObject): The new medicine data.

    Raises:
        ValueError: Invalid data in data argument
        ValueError: Data does not exist in the given data argument
    """
    eu_od_number = data.get("eu_od_number")
    items = data.get(name)
    model_data = model.objects.filter(eu_od_number=eu_od_number).order_by("change_date").first()

    if items is not None and len(items) > 0:
        for item in items:
            if not model_data or item.get(name) != getattr(model_data, name):
                serializer = serializer(
                    None, {
                        name: item.get(name),
                        "change_date": item.get("change_date"),
                        "eu_od_number": eu_od_number
                    }
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(f"{name} contains invalid data! {serializer.errors}")
