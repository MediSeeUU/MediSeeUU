from django.forms.models import model_to_dict
from api.models.get_dashboard_columns import get_initial_history_columns
from api.models.medicine_models import models
from api.models.medicine_models import (
    MedicinalProduct,
    MarketingAuthorisation,
    AcceleratedAssessment,
    Duration,
    HistoryAuthorisationStatus,
    HistoryAuthorisationType,
    HistoryBrandName,
    HistoryMAH,
    HistoryOD,
    HistoryPrime,
    HistoryEUOrphanCon,
    LegalBases,
)
from api.models.other import MedicineLocks
from api.serializers.medicine_serializers.scraper.post.human import (
    MedicinalProductSerializer,
    IngredientsAndSubstancesSerializer,
    MarketingAuthorisationSerializer,
    AcceleratedAssessmentSerializer,
    DurationSerializer,
    ProceduresSerializer,
    LegalBasesSerializer,
    AuthorisationStatusSerializer,
    AuthorisationTypeSerializer,
    BrandNameSerializer,
    MAHSerializer,
    OrphanDesignationSerializer,
    PrimeSerializer,
    EUOrphanConSerializer,
    LegalBasesSerializer,
)
from api.serializers.medicine_serializers.scraper.update.human import (
    MedicinalProductFlexVarUpdateSerializer,
    IngredientsAndSubstancesFlexVarUpdateSerializer,
    MarketingAuthorisationFlexVarUpdateSerializer,
    AcceleratedAssessmentFlexVarUpdateSerializer,
    DurationFlexVarUpdateSerializer,
)
from api.models.other import MedicineLocks


def post(data):
    if eu_pnumber := data.get("eu_pnumber"):
        override = data.get("override")
        # check if medicine already exists based on eu_pnumber
        current_medicine = MedicinalProduct.objects.filter(
            eu_pnumber=eu_pnumber
        ).first()
        # if the medicine doesn't exist or the medicine should be overriden, call add_medicine,
        # otherwise update the flexible variables and the null values

        # if variable is locked, delete it from the data
        locks = MedicineLocks.objects.filter(
            eu_pnumber=eu_pnumber
        ).values_list("column_name", flat=True)

        data = {key: value for key, value in data.items() if key not in locks}

        initial_history_data = {}
        # Remove initial history from medicine and add them later to the database,
        # because of circular dependency
        for initial_history_column in get_initial_history_columns(models):
            if initial_history_column in data:
                initial_history_data[initial_history_column] = \
                    data.pop(initial_history_column)

        if current_medicine is None or override:
            add_or_override_medicine(data, current_medicine)
        else:
            update_flex_medicine(data, current_medicine)
            update_null_values_medicine(data, current_medicine)
        medicine_history_variables(data)
        medicine_list_variables(data)


def update_flex_medicine(data, current):
    """
    This function updates the flexible medicine variables if this is applicable for the current data.
    The function is called if a previous version of the medicine already exists in the database.

    Args:
        data (medicineObject): The new medicine data.
        current (medicineObject): The medicine data that is currently in the database.
    """
    medicine_serializer = MedicinalProductFlexVarUpdateSerializer(current, data=data, partial=True)

    # update medicine
    if medicine_serializer.is_valid():
        medicine_serializer.save()
    else:
        raise ValueError(medicine_serializer.errors)


def add_or_override_medicine(data, current_medicine):
    """
    Adds a new medicine with its attributes to the database. If this is valid,
    it will also add the history variables to the database.

    Args:
        data (medicineObject): The new medicine data.
        current_medicine (medicineObject): The medicine data that is currently in the database.

    Raises:
        ValueError: Invalid data in data argument
    """
    # initialise serializers for addition
    serializer = MedicinalProductSerializer(current_medicine, data=data, partial=True)

    # add medicine and authorisation
    if serializer.is_valid():
        serializer.save()
    else:
        raise ValueError(serializer.errors)


def update_null_values_medicine(data, current_medicine):
    """
    Updates all null values for an existing medicine using the data given in its
    argument "data".

    Args:
        data (medicineObject): The new medicine data.
        current_medicine (medicineObject): The medicine data that is currently in the database.
    """
    medicine = model_to_dict(current_medicine)
    new_data = {"eu_pnumber": data.get("eu_pnumber")}

    for attr in medicine:
        if (getattr(current_medicine, attr) is None or getattr(current_medicine, attr) == '') and (
                not (data.get(attr) is None)
        ):
            new_data[attr] = data.get(attr)

    if len(new_data.keys()) > 1:
        add_or_override_medicine(new_data, current_medicine)


def medicine_list_variables(data):
    """
    Creates new list variables for the history models using the data given in its
    argument "data". It expects the input data for the list variable to be formed like this:
    ``name: ["value1", "value2", ...]``

    Args:
        data (medicineObject): The new medicine data.
    """
    add_medicine_list(
        LegalBases,
        LegalBasesSerializer,
        "eu_legal_basis",
        data,
        True,
    )


def add_medicine_list(model, serializer, name, data, replace):
    """
    Add a new object to the given list model.

    Args:
        model (medicine_model): The list model of the list object you want to add.
        serializer (medicine_serializer): The applicable serializer.
        name (string): The name of the attribute.
        data (medicineObject): The new medicine data.
        replace (bool): If True, will delete all previously added objects with the same eu_pnumber

    Raises:
        ValueError: Invalid data in data argument
        ValueError: Data does not exist in the given data argument
    """
    eu_pnumber = data.get("eu_pnumber")
    items = data.get(name)
    model_data = model.objects.filter(eu_pnumber=eu_pnumber).all()

    if items is not None and len(items) > 0:
        for item in items:
            if model_data and replace:
                model_data.delete()
            serializer = serializer(
                None, {name: item, "eu_pnumber": eu_pnumber}
            )
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError(f"{name} contains invalid data! {serializer.errors}")


def medicine_history_variables(data):
    """
    Creates new history variables for the medicinal product history models using the data given in its
    argument "data". It expects the input data for the history variable to be formed like this:
    ``name: [{name: value, change_date: date}, ...]``

    Args:
        data (medicineObject): The new medicine data.
    """
    add_medicine_history(
        HistoryAuthorisationType,
        AuthorisationTypeSerializer,
        "eu_aut_type",
        data,
    )

    add_medicine_history(
        HistoryAuthorisationStatus,
        AuthorisationStatusSerializer,
        "eu_aut_status",
        data,
    )

    add_medicine_history(
        HistoryBrandName,
        BrandNameSerializer,
        "eu_brand_name",
        data,
    )

    add_medicine_history(
        HistoryOD,
        OrphanDesignationSerializer,
        "eu_od",
        data,
    )

    add_medicine_history(
        HistoryPrime,
        PrimeSerializer,
        "eu_prime",
        data,
    )

    add_medicine_history(
        HistoryMAH,
        MAHSerializer,
        "eu_mah",
        data,
    )

    add_medicine_history(
        HistoryEUOrphanCon,
        EUOrphanConSerializer,
        "eu_orphan_con",
        data,
    )


def add_medicine_history(model, serializer, name, data):
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
    eu_pnumber = data.get("eu_pnumber")
    items = data.get(name)
    model_data = model.objects.filter(eu_pnumber=eu_pnumber).order_by("change_date").first()

    if items is not None and len(items) > 0:
        for item in items:
            if not model_data or item.get(name) != getattr(model_data, name):
                serializer = serializer(
                    None, {name: item.get(name), "change_date": item.get("change_date"), "eu_pnumber": eu_pnumber}
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise ValueError(f"{name} contains invalid data! {serializer.errors}")
