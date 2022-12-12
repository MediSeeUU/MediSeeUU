from django.forms.models import model_to_dict
from api.models.human_models import (
    MedicinalProduct,
    IngredientsAndSubstances,
    MarketingAuthorisation,
    AcceleratedAssessment,
    Duration,
    Procedures,
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
        # if variable is locked, delete it from the data
        locks = MedicineLocks.objects.filter(
            eu_pnumber=eu_pnumber
        ).values_list("column_name", flat=True)

        data = {key: value for key, value in data.items() if key not in locks}

        current_ingredients_and_substances = None
        if active_substance := data.get("active_substance"):
            current_ingredients_and_substances = IngredientsAndSubstances.objects.filter(
                active_substance=active_substance
            ).first()
        data["ingredients_and_substances"] = \
            insert_data(data, current_ingredients_and_substances, IngredientsAndSubstancesFlexVarUpdateSerializer) \
            if current_ingredients_and_substances else \
            insert_data(data, current_ingredients_and_substances, IngredientsAndSubstancesSerializer)

        current_marketing_authorisation = MarketingAuthorisation.objects.filter(
            eu_pnumber=eu_pnumber
        ).first()

        add_or_update_foreign_key(
            data,
            current_marketing_authorisation,
            AcceleratedAssessment,
            AcceleratedAssessmentSerializer,
            AcceleratedAssessmentFlexVarUpdateSerializer,
            "ema_accelerated_assessment"
        )
        add_or_update_foreign_key(
            data,
            current_marketing_authorisation,
            Duration,
            DurationSerializer,
            DurationFlexVarUpdateSerializer,
            "duration"
        )

        insert_data(data, current_marketing_authorisation, MarketingAuthorisationSerializer)

        current_medicinal_product = MarketingAuthorisation.objects.filter(
            eu_pnumber=eu_pnumber
        ).first()

        insert_data(data, current_medicinal_product, MedicinalProductSerializer)

        history_variables(data)
        list_variables(data)


def add_or_update_foreign_key(data, current, related_model, insert_serializer, update_serializer, attribute):
    if current:
        if hasattr(current, attribute):
            if foreign_key := getattr(current, attribute):
                current_related = related_model.objects.filter(
                    id=foreign_key
                ).first()
                if current_related:
                    data[attribute] = insert_data(data, current_related, update_serializer)
                    return None
    data[attribute] = insert_data(data, None, insert_serializer)


def insert_data(data, current, serializer):
    """
    This function updates the flexible medicine variables if this is applicable for the current data.
    The function is called if a previous version of the medicine already exists in the database.

    Args:
        data (medicineObject): The new medicine data.
        current (medicineObject): The medicine data that is currently in the database.
        serializer
    """
    medicine_serializer = serializer(current, data=data, partial=True)

    # update medicine
    if medicine_serializer.is_valid():
        inserted = medicine_serializer.save()
        return inserted.pk
    else:
        raise ValueError(medicine_serializer.errors)


def add_or_override_medicine(data, eu_pnumber):
    """
    Adds a new medicine with its attributes to the database. If this is valid,
    it will also add the history variables to the database.

    Args:
        data (medicineObject): The new medicine data.
        eu_pnumber (str): The EU number of the human medicine being added

    Raises:
        ValueError: Invalid data in data argument
    """
    # initialise serializers for addition
    current_medicine = MedicinalProduct.objects.filter(
        eu_pnumber=eu_pnumber
    ).first()
    serializer = MedicinalProductSerializer(current_medicine, data=data, partial=True)

    # add medicine and authorisation
    if serializer.is_valid():
        serializer.save()
    else:
        raise ValueError(serializer.errors)


def update_null_values(data, current_medicine):
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


def list_variables(data):
    """
    Creates new list variables for the history models using the data given in its
    argument "data". It expects the input data for the list variable to be formed like this:
    ``name: ["value1", "value2", ...]``

    Args:
        data (medicineObject): The new medicine data.
    """
    add_list(
        LegalBases,
        LegalBasesSerializer,
        "eu_legal_basis",
        data,
        True,
    )


def add_list(model, serializer, name, data, replace):
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


def history_variables(data):
    """
    Creates new history variables for the medicinal product history models using the data given in its
    argument "data". It expects the input data for the history variable to be formed like this:
    ``name: [{name: value, change_date: date}, ...]``

    Args:
        data (medicineObject): The new medicine data.
    """
    add_history(
        HistoryAuthorisationType,
        AuthorisationTypeSerializer,
        "eu_aut_type",
        data,
    )

    add_history(
        HistoryAuthorisationStatus,
        AuthorisationStatusSerializer,
        "eu_aut_status",
        data,
    )

    add_history(
        HistoryBrandName,
        BrandNameSerializer,
        "eu_brand_name",
        data,
    )

    add_history(
        HistoryOD,
        OrphanDesignationSerializer,
        "eu_od",
        data,
    )

    add_history(
        HistoryPrime,
        PrimeSerializer,
        "eu_prime",
        data,
    )

    add_history(
        HistoryMAH,
        MAHSerializer,
        "eu_mah",
        data,
    )

    add_history(
        HistoryEUOrphanCon,
        EUOrphanConSerializer,
        "eu_orphan_con",
        data,
    )


def add_history(model, serializer, name, data):
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
